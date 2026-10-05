#!/usr/bin/env python3
"""Exact one-sided tangent-cone and optional finite-pair certificates.

All arithmetic is Gaussian rational. A successful first-jet decision is
conditional on a sufficiently small quadratic neighborhood; it does not
infer a curvature bound or local interval for an unspecified curve. Optional
per-component remainder budgets certify one supplied pair only. A support
opening additionally supplies an exact impossible-event probability.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s
from matrix_metric import (require, strict_keys, positive_integer, rational,
    gaussian, matrix_from_json, matrix_to_json, is_positive_semidefinite as psd)
from finite_outcome_certificate import matrix_tuple_legal
from support_geometry import support, support_data

INPUT='gtf86.one-sided-jet/1'
CERT='gtf86.cone-certificate/1'


def classify(effects, direction):
    require(type(effects) is list and len(effects)>=2,'at least two effects required')
    e=[s.Matrix(a).applyfunc(gaussian) for a in effects]
    require(matrix_tuple_legal(e,False),'illegal measurement')
    d=e[0].rows;z=s.zeros(d)
    require(type(direction) is list and len(direction)==len(e),'wrong direction count')
    h=[s.Matrix(a).applyfunc(gaussian) for a in direction]
    require(all(a.shape==(d,d) and a==a.adjoint() for a in h),'non-Hermitian or wrong-size direction')
    require(sum(h,z)==z,'direction sum is not zero')
    p=[support(a) for a in e];q=[s.eye(d)-a for a in p]
    j=[(a*b*a).applyfunc(gaussian) for a,b in zip(q,h)]
    require(all(psd(a) for a in j),'direction not in one-sided cone: negative missing-support block')
    lineality=all(a==z for a in j)
    gamma=(s.I*sum((a*b-b*a for a,b in zip(p,h)),z)/2).applyfunc(gaussian)
    data=support_data(e,gamma)
    nonzero=any(a!=z for a in h)
    in_range=lineality and data['in_span']
    mode=('higher_order_undetermined' if not nonzero else
          'support_opening' if not lineality else
          'regular_tangent' if in_range else 'coherent_tangent')
    witness=None
    if not lineality:
        for label,a in enumerate(j):
            for coordinate in range(d):
                if a[coordinate,coordinate]>0:
                    v=q[label][:,coordinate];norm=gaussian((v.adjoint()*v)[0])
                    rate=gaussian((v.adjoint()*h[label]*v)[0]/norm)
                    require(norm>0 and rate>0,'invalid opening witness')
                    witness={'label_index':label,'coordinate_index':coordinate,
                        'vector':matrix_to_json(v),'norm_squared':str(norm),
                        'slope':str(rate),'base_probability':'0'}
                    break
            if witness is not None:break
    return {'effects':e,'direction':h,'supports':p,'missing':j,'lineality':lineality,
        'gamma':gamma,'projected':data['projected'],'residual':data['complement'],
        'kernel_dimension':data['kernel_dimension'],'ranks':data['ranks'],
        'nonzero':nonzero,'in_range':in_range,'mode':mode,'witness':witness}


def parse(raw,max_dimension=256):
    strict_keys(raw,{'schema','dimension','outcomes','effects','direction','pair'},'cone input')
    require(raw['schema']==INPUT,'wrong cone schema')
    d=positive_integer(raw['dimension'],'dimension')
    k=positive_integer(raw['outcomes'],'outcomes')
    cap=positive_integer(max_dimension,'maximum system dimension')
    require(k>=2 and (k-1)*d*d<=cap,'resource cap exceeded: no partial certificate')
    require(type(raw['effects']) is list and len(raw['effects'])==k,'wrong effect count')
    require(type(raw['direction']) is list and len(raw['direction'])==k,'wrong direction count')
    e=[matrix_from_json(x,d,'effect') for x in raw['effects']]
    h=[matrix_from_json(x,d,'direction') for x in raw['direction']]
    return e,h


def check_pair(pair,data):
    if pair is None:return None
    strict_keys(pair,{'effects','scale','remainder_budget','component_budgets'},'finite pair')
    e=data['effects'];h=data['direction'];d=e[0].rows;k=len(e)
    scale=rational(pair['scale'],'scale');budget=rational(pair['remainder_budget'],'remainder budget')
    require(scale>0 and budget>=0,'invalid scale or remainder budget')
    require(type(pair['component_budgets']) is list and len(pair['component_budgets'])==k,
        'wrong component budget count')
    allowances=[rational(x,'component budget') for x in pair['component_budgets']]
    require(all(a>=0 for a in allowances) and sum(allowances)<=budget,'invalid budget allocation')
    require(type(pair['effects']) is list and len(pair['effects'])==k,'wrong pair effect count')
    f=[matrix_from_json(x,d,'pair effect') for x in pair['effects']]
    require(matrix_tuple_legal(f,False),'illegal pair measurement')
    remainder=[(b-a-scale*u).applyfunc(gaussian) for a,b,u in zip(e,f,h)]
    require(all(psd(a*scale**2*s.eye(d)+r) and psd(a*scale**2*s.eye(d)-r)
                for a,r in zip(allowances,remainder)),'finite pair exceeds component allowance')
    probability=None
    if data['witness'] is not None:
        label=data['witness']['label_index'];coordinate=data['witness']['coordinate_index']
        q=s.eye(d)-data['supports'][label];v=q[:,coordinate]
        probability=gaussian((v.adjoint()*f[label]*v)[0]/(v.adjoint()*v)[0])
        require(0<=probability<=1,'invalid exact event probability')
    return {'verified':True,'scale':str(scale),'remainder_budget':str(budget),
        'component_budgets':[str(a) for a in allowances],
        'remainders':[matrix_to_json(a) for a in remainder],
        'opening_event_probability':None if probability is None else str(probability),
        'event_lower_for_any_positive_integer_N':None if probability is None else '2*(1-(1-p)**N)',
        'small_parameter_interval_certified':False,'unspecified_family_remainder_certified':False}


def certify(raw,max_dimension=256):
    e,h=parse(raw,max_dimension);c=classify(e,h);pair=check_pair(raw['pair'],c)
    return {'schema':CERT,'status':'success',
        'input_sha256':hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'dimension':e[0].rows,'outcomes':len(e),'support_ranks':c['ranks'],
        'support_projections':[matrix_to_json(a) for a in c['supports']],
        'missing_support_blocks':[matrix_to_json(a) for a in c['missing']],
        'one_sided_first_order_realizable':True,'two_sided_first_order_realizable':c['lineality'],
        'direction_nonzero':c['nonzero'],'mechanism':c['mode'],
        'support_generator':matrix_to_json(c['gamma']),
        'generator_projection':matrix_to_json(c['projected']),
        'generator_residual':matrix_to_json(c['residual']),
        'direction_in_covariance_range':bool(c['in_range']),
        'covariance_kernel_dimension':c['kernel_dimension'],'opening_witness':c['witness'],
        'adaptive_scale':None if not c['nonzero'] else 'sqrt(N)*s' if c['in_range'] else 'N*s',
        'independent_probe_scale':None if not c['nonzero'] else 'sqrt(N)*s' if c['lineality'] else 'N*s',
        'theorem':None if not c['nonzero'] else 'thm:tubedichotomy86',
        'scope':'fixed E,H,Lambda; sufficiently small quadratic neighborhoods; scales truncated at one',
        'independent_probe_model':'product probe-reference pairs; no feedback; arbitrary joint final readout',
        'finite_pair':pair,'curvature_bound_computed':False,'local_interval_computed':False,
        'arbitrary_pair_covariance_equivalence_claimed':False,
        'stationarity_inferred_from_zero_direction':False,'recovery_synthesized':False,
        'physical_protocol_executed':False,'continuum_proof_by_replay':False}


def verify(raw,certificate,max_dimension=256):
    require(type(certificate) is dict and json.dumps(certificate,sort_keys=True,separators=(',',':'))==json.dumps(certify(raw,max_dimension),sort_keys=True,separators=(',',':')),
        'cone certificate differs from full exact reconstruction')
    return {'schema':'gtf86.cone-verification/1','status':'success','complete_exact_replay':True,
        'physical_protocol_executed':False,'continuum_proof_by_replay':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('--verify',type=Path)
    parser.add_argument('--max-system-dimension',type=int,default=256);args=parser.parse_args()
    try:
        raw=json.loads(args.input.read_text())
        output=verify(raw,json.loads(args.verify.read_text()),args.max_system_dimension) if args.verify else certify(raw,args.max_system_dimension)
        print(json.dumps(output,indent=2,sort_keys=True))
    except (ValueError,TypeError,KeyError,OSError,RuntimeError) as error:
        parser.exit(2,'cone geometry: '+str(error)+'\n')

if __name__=='__main__':main()
