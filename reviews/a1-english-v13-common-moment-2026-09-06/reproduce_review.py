#!/usr/bin/env python3
"""Independent v13 request probes and a finite physical floor-stop experiment.

Run: python reproduce_review.py --source-root papers/A1-english-v13 --output EXECUTION_PROBES.json
Only production modules are imported. No author test helper is imported.
This is finite diagnostic evidence, not formal proof verification.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
from hashlib import sha256, sha1
from itertools import product
from pathlib import Path
import json
import sys

PIN = 'fc6465b86fbc7ee6a4e8f3ccfb54ea32a64dc8b6'
MANIFEST_BLOB = 'de4345eb94c864f2e102f4a013f95f1cfc5be1ab'
COUNTS: Counter[str] = Counter()

def check(ok: bool, category: str) -> None:
    if not ok:
        raise AssertionError(category)
    COUNTS[category] += 1

def norm(a, b):
    check(len(a) == len(b), 'independent_dimension_agreement')
    return max((abs(x-y) for x,y in zip(a,b)), default=F(0))

def main(root: Path) -> dict:
    manifest_bytes = (root/'SOURCE_MANIFEST.json').read_bytes()
    blob = sha1(b'blob '+str(len(manifest_bytes)).encode()+b'\0'+manifest_bytes).hexdigest()
    check(blob == MANIFEST_BLOB, 'pinned_manifest_git_blob')
    manifest = json.loads(manifest_bytes)
    for name, digest in manifest['sha256'].items():
        check(sha256((root/name).read_bytes()).hexdigest() == digest, 'source_sha256')
    sys.path.insert(0, str(root.resolve()))
    import certified_compiler as cc
    from construction_contracts import ContractError
    from finite_compiler import Machine

    def grid_factory(b, h, tau=None):
        segments = 1 << max(0, b-2)
        grid = tuple(F(1,4)+F(j,2*segments) for j in range(segments+1))
        def evaluate(history):
            s = F(1,2)
            for u,_ in history:
                s = (s+grid[u])/2
            return (s,)
        return len(grid),evaluate,evaluate,grid

    def fixed_factory(b, h, tau=None):
        grid = (F(1,4),F(1,2),F(3,4))
        def evaluate(history):
            s = F(1,2)
            for u,_ in history:
                s = (s+grid[u])/2
            return (s,)
        return 3,evaluate,evaluate,grid

    def invoke(robust, T, M, factory, A):
        schema = dict(state_dimensions=(1,)*(T+1), query_counts=(1,)*(T+1))
        if robust:
            return cc.robust_adaptive_compile(T,1,M,A,factory,F(1,128),max_bits=14,**schema)
        return cc.adaptive_compile(T,1,M,A,factory,absolute_tolerance=F(1,128),max_bits=14,**schema)

    original = cc.compile_tables
    controls, rejections = [], []
    try:
        for robust in (False, True):
            for M in (1,2):
                cc.compile_tables = original
                p,a,trace,_ = invoke(robust,1,M,grid_factory,F(1,2))
                true_radius = F(1,8*M)
                for row in trace:
                    check(row['lower'] <= true_radius <= row['upper'], 'known_interval_radius_bracket')
                controls.append(dict(robust=robust, M=M, b=trace[-1]['b'], true_radius=true_radius,
                                     final_lower=trace[-1]['lower'], final_upper=trace[-1]['upper']))
                for fault in ('wrong_precision','lying_precision'):
                    def mutated(*args, **kwargs):
                        args = list(args)
                        requested = args[4]
                        args[4] = 0
                        p,a = original(*args, **kwargs)
                        if fault == 'lying_precision':
                            p = replace(p, output_bits=requested)
                        return p,a
                    cc.compile_tables = mutated
                    try:
                        invoke(robust,1,M,grid_factory,F(1,2))
                    except ContractError as exc:
                        check(True, 'precision_fault_rejected')
                        rejections.append(dict(robust=robust,M=M,fault=fault,error=str(exc)))
                    else:
                        raise AssertionError('precision mutation accepted')
                cc.compile_tables = original
            def shortened(*args, **kwargs):
                args = list(args); args[0] = 1
                return original(*args, **kwargs)
            cc.compile_tables = shortened
            try:
                invoke(robust,2,2,fixed_factory,F(0))
            except ContractError as exc:
                check(True, 'short_horizon_rejected')
                rejections.append(dict(robust=robust,fault='short_horizon',error=str(exc)))
            else:
                raise AssertionError('short horizon accepted')
    finally:
        cc.compile_tables = original

    # Independent exponent-keyed physical truth, not the formal-label compiler algebra.
    def mul(p, q):
        out = {}
        for x,c in p.items():
            for y,d in q.items():
                out[x+y] = out.get(x+y,F(0))+c*d
        return {x:c for x,c in out.items() if c}

    def labels(degree):
        return tuple((i,j,degree-i-j) for i in range(degree+1) for j in range(degree-i+1))

    C = ((F(1,3),-F(1,16),-F(1,16)),(F(1,3),F(1,16),F(0)),(F(1,3),F(0),F(1,16)))
    commands = ((F(1,4),F(3,4),F(1,4)),(F(3,4),F(1,4),F(3,4)))
    delta = F(1,1<<26)
    models = ((F(0),delta/2),(F(0),-delta/2),(-delta/4,F(0)),(delta/4,F(0)))
    all_labels = tuple(a for n in range(4) for a in labels(n))
    name = {a:F(1,1+a[1]+2*a[2]) + (-1 if i%2==0 else 1)*delta/8
            for i,a in enumerate(all_labels)}

    def moment(s, tilt):
        return 1/(1+s)+tilt*(1/(2+s)-1/(2*(1+s)))

    def truth(history, gap, tilt):
        exponents = (F(0),F(1),F(2)+gap)
        likelihood = {F(0):F(1)}
        for u,x in history:
            g = commands[u]
            row = tuple(g[x]*v for v in C[x]) if x<3 else tuple(
                sum((1-g[j])*C[j][i] for j in range(3)) for i in range(3))
            likelihood = mul(likelihood,dict(zip(exponents,row)))
        def integral(poly):
            return sum(c*moment(s,tilt) for s,c in poly.items())
        z = integral(likelihood)
        remaining = 3-len(history)
        raw = tuple(integral(mul(likelihood,{sum(v*a for v,a in zip(exponents,alpha)):F(1)}))/z
                    for alpha in labels(remaining))
        basis = ({F(0):F(1,2)}, {F(0):F(1,2),F(1):F(1,32)},
                 {F(0):F(1,2),F(2)+gap:F(1,32)})
        query = []
        for word in product(basis,repeat=remaining):
            q = likelihood
            for factor in word:
                q = mul(q,factor)
            query.append(integral(q)/z)
        return raw,tuple(query)

    alphabet = tuple(product(range(2),range(4)))
    histories = tuple(tuple(product(alphabet,repeat=n)) for n in range(3))
    advice = cc.MomentAdvice(C,name,commands,3,delta,F(2),F(1,32))
    actual_raw_error = F(0)
    for gap,tilt in models:
        for alpha in all_labels:
            s = alpha[1]+(2+gap)*alpha[2]
            check(abs(name[alpha]-moment(s,tilt)) <= delta, 'physical_common_name_compatibility')
        for hs in histories:
            for history in hs:
                raw, query = truth(history,gap,tilt)
                actual_raw_error = max(actual_raw_error,norm(raw,advice.state(history)),
                                       norm(query,advice.predictions(history)))
    rho = 2*advice.max_quotient_bound
    check(0<rho<1, 'positive_advice_floor')
    check(actual_raw_error <= rho/2, 'independent_callback_accuracy')
    name_digest = sha256(repr(tuple(name.items())).encode()).hexdigest()
    def factory(b,h,tau):
        check(sha256(repr(tuple(name.items())).encode()).hexdigest()==name_digest, 'unchanged_common_name')
        check(advice.max_quotient_bound <= tau/2, 'external_input_error_budget')
        return 2,advice.state,advice.predictions,None
    # M=64 covers every candidate at both stages, so the exact finite-domain radius is zero.
    p,a,trace,_ = cc.robust_adaptive_compile(2,4,64,F(0),factory,rho,max_bits=22,
                                           state_dimensions=(10,6,3),query_counts=(27,9,3))
    digest = sha256(repr(p).encode()).hexdigest()
    last = trace[-1]
    check(last['floor_stop'] and not last['radius_stop'], 'physical_floor_only_stop')
    check(p.state_counts == (1,8,64), 'full_finite_candidate_budget')
    check(last['r']==0, 'zero_finite_cover_radius')
    for row in trace:
        check(row['lower']<=0<=row['upper'], 'zero_radius_bracket')
    tau = last['tau']
    # Coefficient l1 <=1 and report likelihood >=1/32 give a raw-state Lipschitz bound 64.
    E = (F(0),2*tau,130*tau)
    per_model = []
    for gap,tilt in models:
        error = F(0)
        for history in histories[2]:
            machine = Machine(); prefix = ()
            for n,(u,x) in enumerate(history):
                machine.step(p,n,u,x); prefix += ((u,x),)
                raw,query = truth(prefix,gap,tilt)
                representative = truth(a.representatives[n+1][machine.index],gap,tilt)[0]
                check(norm(raw,representative)<=E[n+1], 'independent_physical_state_recurrence')
                for j,target in enumerate(query):
                    difference = abs(machine.output(p,n+1,j)-target)
                    check(difference <= E[n+1]+tau, 'independent_all_query_physical_error')
                    error = max(error,difference)
        check(sha256(repr(p).encode()).hexdigest()==digest,'one_unchanged_program_for_all_models')
        per_model.append(dict(gap=gap,prior_tilt=tilt,paths=64,maximum_query_error=error))
    return dict(status='passed',submission_sha=PIN,source_files_verified=len(manifest['sha256']),
                source_manifest_git_blob=blob,assertions=sum(COUNTS.values()),categories=dict(COUNTS),
                interval_controls=controls,request_faults_rejected=rejections,
                physical_floor=dict(M=64,delta=delta,rho=rho,actual_raw_error=actual_raw_error,
                    name_sha256=name_digest,program_sha256=digest,state_counts=p.state_counts,
                    final_scale=last,trace_length=len(trace),models=per_model),
                scope='Exact rational finite two-command/four-report experiment, N=3/T=2. '
                      'Floor-stop diagnostic only; not full-cube, N=5 phase, or formal proof validation.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    data = main(args.source_root)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2,default=str)+'\n')
    print(json.dumps({'status':data['status'],'assertions':data['assertions'],
                      'faults_rejected':len(data['request_faults_rejected']),
                      'physical_floor_b':data['physical_floor']['final_scale']['b']},indent=2))
