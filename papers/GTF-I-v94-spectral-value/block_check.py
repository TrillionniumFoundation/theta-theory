#!/usr/bin/env python3
"""Exact finite block-law, nonempty-realization and replay regressions.

Full small GHZ probability tables are evaluated for a concrete two-outcome
projective measurement family. They do not execute or verify the universal
correcting recovery, a physical device, or a continuum theorem.
"""
from __future__ import annotations
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import sympy as s
import block_geometry as b
from matrix_metric import require, matrix_to_json, is_positive_semidefinite as psd
from finite_outcome_certificate import matrix_tuple_legal

checks=[];rejections=[];laws=[];plans=[]

def ok(value,name):
    require(bool(value),'block regression failed: '+name);checks.append(name)

def reject(fn,name):
    try:fn()
    except (ValueError,TypeError,KeyError,RuntimeError):rejections.append(name);return
    raise RuntimeError('negative control accepted: '+name)

def raw(e,h,pair=None):
    return {'schema':b.INPUT,'dimension':e[0].rows,'outcomes':len(e),
            'effects':[matrix_to_json(x) for x in e],
            'direction':[matrix_to_json(x) for x in h],'pair':pair}

def kron(items):
    r=s.ones(1)
    for a in items:r=s.kronecker_product(r,a)
    return r

def compositions(n):
    if n==0:yield ();return
    for first in range(1,n+1):
        for tail in compositions(n-first):yield (first,)+tail

def main():
    I=s.eye(2);P=s.diag(1,0);X=s.Matrix([[0,1],[1,0]])
    Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    fixtures=[([P,I-P],[Y,-Y],'coherent_tangent'),
              ([I/2,I/2],[Z/4,-Z/4],'regular_tangent'),
              ([I/2,I/2,s.zeros(2)],[-I/2,-I/2,I],'support_opening'),
              ([P,I-P],[s.zeros(2),s.zeros(2)],'higher_order_undetermined')]
    E3=[s.diag(1,0,0),s.diag(0,1,1)]
    H3=s.Matrix([[0,0,1],[0,1,0],[1,0,0]])
    fixtures.append((E3,[H3,-H3],'support_opening'))
    for idx,(e,h,mode) in enumerate(fixtures):
        inp=raw(e,h);cert=b.certify(inp);data=b.cone.classify(e,h)
        ok(cert['mechanism']==mode,f'mechanism-{idx}')
        ok(b.verify(inp,cert)['complete_exact_replay'],f'replay-{idx}')
        r=cert['nonempty_realization'];lim=s.Rational(r['realization_interval_upper'])
        coeff=s.Rational(r['component_allowance'])
        a=s.Rational(r['tangent_norm_upper']);lam=s.Rational(r['positive_support_floor'])
        for j,(ej,hj,pj) in enumerate(zip(e,h,data['supports'])):
            ok(psd(ej-lam*pj),f'support-floor-{idx}-{j}')
            ok(psd(a*s.eye(ej.rows)+hj) and psd(a*s.eye(ej.rows)-hj),f'tangent-bound-{idx}-{j}')
        for frac in (s.Rational(0),s.Rational(1,4),s.Rational(1,2),s.Rational(1)):
            t=lim*frac;f=b.realized_tuple(data,t,r)
            ok(matrix_tuple_legal(f,False),f'legal-curve-{idx}-{frac}')
            for j,(fj,ej,hj) in enumerate(zip(f,e,h)):
                R=fj-ej-t*hj;bound=coeff*t*t*s.eye(ej.rows)
                ok(psd(bound+R) and psd(bound-R),f'finite-remainder-{idx}-{frac}-{j}')
        bad=deepcopy(cert);bad['nonempty_realization']['positive_support_floor']='2'
        reject(lambda:b.verify(inp,bad),f'changed-floor-{idx}')
    inp=json.loads((Path(__file__).parent/'examples/entanglement-width-projective.json').read_text())
    cert=b.certify(inp)
    ok(cert['cone_certificate']['finite_pair']['verified'],'supplied-projective-pair')
    ok(cert['block_scale']=='sqrt(N*b)*s' and cert['parallel_scale']=='N*s','parallel-not-product-rate')
    for key in ('exact_distance_computed','recovery_synthesized','physical_protocol_executed','continuum_proof_by_replay'):
        ok(cert[key] is False,'scope-'+key)
    bad=deepcopy(cert);bad['parallel_scale']='sqrt(N)*s'
    reject(lambda:b.verify(inp,bad),'wrong-parallel-scaling')
    bad=deepcopy(cert);bad['nonempty_realization']['minimal_allowance_claimed']=True
    reject(lambda:b.verify(inp,bad),'minimality-overclaim')
    bad=deepcopy(cert);bad['physical_protocol_executed']=True
    reject(lambda:b.verify(inp,bad),'physical-execution-overclaim')
    reject(lambda:b.certify(inp,max_system_dimension=1),'dimension-cap')
    reject(lambda:b.certify(inp,max_system_dimension=True),'boolean-cap')
    reject(lambda:b.certify(inp,max_halvings=0),'zero-halving-cap')
    small=raw([s.diag(s.Rational(1,257),0),I-s.diag(s.Rational(1,257),0)],[Y,-Y])
    reject(lambda:b.certify(small,max_halvings=2),'support-floor-cap-exhaustion')
    ok(s.Rational(b.certify(small)['nonempty_realization']['positive_support_floor'])<=s.Rational(1,257),'small-positive-eigenvalue')
    for mutation,name in [({'unexpected':0},'extra-key'),({'schema':'bad'},'wrong-schema'),({'outcomes':True},'boolean-outcomes')]:
        bad=dict(inp,**mutation);reject(lambda:b.certify(bad),name)
    reject(lambda:b.certify(raw([P,I-P],[-(I-P),I-P])),'negative-missing-support')
    reject(lambda:b.certify(raw([P,I-P],[X,X])),'nonzero-tangent-sum')
    reject(lambda:b.certify(raw([P,I-P],[s.Matrix([[0,1],[0,0]]),-s.Matrix([[0,1],[0,0]])])),'nonhermitian-tangent')
    bad=deepcopy(inp);bad['effects'][0][0][0][0]='2/2'
    reject(lambda:b.certify(bad),'noncanonical-rational')
    data=b.cone.classify([P,I-P],[Y,-Y]);r=b.realization_data(data)
    reject(lambda:b.realized_tuple(data,2,r),'outside-realization-interval')
    bad=deepcopy(inp);bad['pair']['component_budgets']=['0','0']
    reject(lambda:b.certify(bad),'false-pair-allowance')

    # Complete physical probability tables, computed exactly, for pre-entangled
    # probes and simultaneous local measurements. No sequential correction used.
    plus=s.Matrix([1,1])/s.sqrt(2);minus=s.Matrix([1,-1])/s.sqrt(2)
    for m,t in product(range(1,5),(s.Rational(1,8),s.Rational(1,16),s.Rational(1,32))):
        psi=(kron([plus]*m)-s.I*kron([minus]*m))/s.sqrt(2)
        f0=s.Matrix([[1,-s.I*t],[s.I*t,t*t]])/(1+t*t);f=[f0,I-f0]
        w=(1+s.I*t)**2/(1+t*t);signal=s.simplify(s.im(s.expand_complex(w**m)))
        probs=[];base_probs=[]
        for bits in product((0,1),repeat=m):
            probability=s.simplify((psi.adjoint()*kron([f[j] for j in bits])*psi)[0])
            base=s.simplify((psi.adjoint()*kron([[P,I-P][j] for j in bits])*psi)[0])
            expected=(1+(-1)**sum(bits)*signal)/2**m
            ok(probability==expected and probability>=0,f'GHZ-full-law-{m}-{t}-{bits}')
            ok(base==s.Rational(1,2**m),f'GHZ-base-law-{m}-{t}-{bits}')
            probs.append(probability);base_probs.append(base)
        ok(sum(probs)==1,f'GHZ-normalization-{m}-{t}')
        l1=sum(abs(x-y) for x,y in zip(probs,base_probs))
        ok(l1==abs(signal),f'GHZ-parity-sufficient-{m}-{t}')
        laws.append({'calls':m,'rational_rotation_parameter':str(t),'outcome_strings':2**m,
                     'parity_signal':str(signal),'l1_separation':str(l1)})
    # Explicit rational checks of tensor-product error accumulation.
    for m,p in product(range(1,17),(s.Rational(1,256),s.Rational(1,64))):
        ok(0<=1-(1-p)**m<=m*p,f'tensor-remainder-{m}-{p}')
    for N in range(1,7):
        for ns in compositions(N):
            probs=[s.Rational(n*n,1024) for n in ns]
            ok(1-s.prod(1-p for p in probs)<=sum(probs),f'fidelity-product-bound-{ns}')
            ok(sum(n*n for n in ns)<=N*max(ns),f'partition-second-moment-{ns}')
    # All floor transitions in the lower-bound block choice, not just b=N.
    for N in (1,2,3,7,16,31):
        for width in sorted({1,min(3,N),N}):
            for u in (s.Rational(1,4),s.Rational(1,16),s.Rational(1,64)):
                m=min(width,int(s.floor(1/(2*u))));ell=N//m;x=m*u
                ok(1<=m<=width and ell*m<=N and ell>=s.Rational(N,2*m),f'block-budget-{N}-{width}-{u}')
                ok(0<x<=s.Rational(1,2),f'phase-upper-{N}-{width}-{u}')
                ok((m==width) or x>=s.Rational(1,4),f'phase-truncation-{N}-{width}-{u}')
                plans.append({'N':N,'b':width,'s_times_gap':str(u),'m':m,'blocks':ell})
    return {'schema':'gtf87.block-regression/1','status':'success',
        'positive_checks':len(checks),'negative_controls':len(rejections),
        'complete_parallel_probability_laws':laws,'integer_block_plans':plans,
        'checks':checks,'rejection_controls':rejections,
        'general_recovery_synthesized':False,'physical_protocol_executed':False,
        'continuum_theorems_proved_by_tests':False,'priority_certified':False}

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
