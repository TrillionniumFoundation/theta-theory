#!/usr/bin/env python3
"""Exact tangent-mechanism and sufficient nonempty-tube certificates.

The block/parallel rates are applications of the written theorem, not computed
trace distances. The interval below certifies only an explicit legal rational
realization, not the small interval for discrimination or a curvature bound.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s
from matrix_metric import (require, positive_integer, gaussian,
    matrix_to_json, is_positive_semidefinite as psd)
import cone_geometry as cone

INPUT='gtf87.entanglement-width/1'
CERT='gtf87.width-certificate/1'


def realization_data(data, max_halvings=512):
    cap=positive_integer(max_halvings,'support-floor halving cap')
    e,h,p=data['effects'],data['direction'],data['supports']
    d=e[0].rows;k=len(e)
    a=max(s.Integer(1),max(sum(abs(s.re(z))+abs(s.im(z)) for z in u.row(i))
                         for u in h for i in range(d)))
    lam=s.Integer(1)
    for halvings in range(cap+1):
        if all(psd(u-lam*v) for u,v in zip(e,p)):break
        require(halvings<cap,'support-floor cap exhausted: no partial certificate')
        lam/=2
    c=1+2*a*a/lam
    limit=min(s.Integer(1),lam/(2*a),1/a)
    allowance=c*k*(1+2*k)
    return {'tangent_norm_upper':str(a),'positive_support_floor':str(lam),
            'halvings':halvings,'quadratic_shift':str(c),
            'realization_interval_upper':str(limit),'sufficient_allowance':str(allowance),
            'component_allowance':str(c*(1+2*k)),
            'formula':'(E_j+s*H_j+c*s^2*I)/(1+k*c*s^2)',
            'coefficient_field':'Gaussian rationals',
            'nonemptiness_for_allowance_at_least_this_value':True,
            'minimal_allowance_claimed':False,
            'discrimination_interval_computed':False}


def realized_tuple(data, scale, certificate):
    """Evaluate only the certified explicit curve on its certified interval."""
    t=cone.rational(str(scale),'realization scale')
    limit=s.Rational(certificate['realization_interval_upper'])
    require(0<=t<=limit,'outside certified realization interval')
    c=s.Rational(certificate['quadratic_shift']);e=data['effects'];h=data['direction']
    k=len(e);eye=s.eye(e[0].rows)
    return [((u+t*v+c*t*t*eye)/(1+k*c*t*t)).applyfunc(gaussian) for u,v in zip(e,h)]


def certify(raw,max_system_dimension=256,max_halvings=512):
    require(type(raw) is dict and raw.get('schema')==INPUT,'wrong width input schema')
    old=dict(raw,schema=cone.INPUT)
    e,h=cone.parse(old,max_system_dimension)
    data=cone.classify(e,h);base=cone.certify(old,max_system_dimension)
    realized=realization_data(data,max_halvings)
    mode=data['mode'];rates={
        'regular_tangent':('sqrt(N)*s','sqrt(N)*s'),
        'coherent_tangent':('sqrt(N*b)*s','N*s'),
        'support_opening':('N*s','N*s'),
        'higher_order_undetermined':(None,None)}
    blocks,parallel=rates[mode]
    return {'schema':CERT,'status':'success',
        'input_sha256':hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'mechanism':mode,'cone_certificate':base,'nonempty_realization':realized,
        'block_scale':blocks,'parallel_scale':parallel,
        'adaptive_scale':base['adaptive_scale'],'rates_truncated_at_one':True,
        'integer_resource_range':'1 <= b <= N',
        'resource_model':'Independent complete probe-reference blocks of at most b calls; no input feedback; arbitrary final joint processing; public mixing allowed.',
        'rate_scope':'Fixed E,H nonzero,Lambda; all legal pairs in the quadratic tube; sufficiently small s, uniformly in N,b and the remainder.',
        'rate_theorem':None if blocks is None else 'thm:widthlaw87',
        'parallel_theorem':None if blocks is None else 'cor:parallel87',
        'exact_distance_computed':False,'recovery_synthesized':False,
        'curvature_of_unspecified_family_computed':False,
        'physical_protocol_executed':False,'continuum_proof_by_replay':False,
        'firstness_or_priority_certified':False}


def verify(raw,certificate,max_system_dimension=256,max_halvings=512):
    expected=certify(raw,max_system_dimension,max_halvings)
    require(type(certificate) is dict and
        json.dumps(certificate,sort_keys=True,separators=(',',':'))==
        json.dumps(expected,sort_keys=True,separators=(',',':')),
        'width certificate differs from complete exact reconstruction')
    return {'schema':'gtf87.width-verification/1','status':'success',
        'complete_exact_replay':True,'physical_protocol_executed':False,
        'continuum_proof_by_replay':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('--verify',type=Path)
    parser.add_argument('--max-system-dimension',type=int,default=256)
    parser.add_argument('--max-halvings',type=int,default=512);args=parser.parse_args()
    try:
        raw=json.loads(args.input.read_text())
        result=(verify(raw,json.loads(args.verify.read_text()),args.max_system_dimension,args.max_halvings)
                if args.verify else certify(raw,args.max_system_dimension,args.max_halvings))
        print(json.dumps(result,indent=2,sort_keys=True))
    except (ValueError,TypeError,KeyError,OSError,RuntimeError) as exc:
        parser.exit(2,'block geometry: '+str(exc)+'\n')

if __name__=='__main__':main()
