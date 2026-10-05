#!/usr/bin/env python3
"""Exact hard quadratic-budget witnesses; no physical reset calibration.

The run-length witness is polynomial in represented integer size. It does not
expand N singleton blocks. A supplied policy is checked completely as a DAG.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any
import feedback_budget as legacy


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def canonical(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def budget_witness(N: int, Q: int) -> dict[str, Any]:
    require(type(N) is int and type(Q) is int and N >= 1 and N <= Q <= N*N,
            'require genuine integers N>=1 and N<=Q<=N^2')
    b = Q//N
    full, rest = divmod(N, b)
    V = full*b*b+rest*rest
    require(N <= V <= Q and 4*V >= Q, 'invalid constructive cost ledger')
    return {'calls':N, 'quadratic_budget':Q, 'width':b, 'realized_square_cost':V,
            'run_length':{'full_blocks':full,'block_size':b,'residual':rest},
            'quarter_budget_attained':True,
            'every_integer_budget_exactly_attained':False}


def analyze(data: dict[str, Any], *, max_nodes: int = 10000) -> dict[str, Any]:
    require(type(data) is dict and set(data) <= {'schema','N','Q','policy','reset_defects'}
            and {'schema','N','Q'} <= set(data), 'unexpected input fields')
    require(data['schema'] == 'gtf89.quadratic-input/1', 'unknown input schema')
    require(type(max_nodes) is int and max_nodes > 0, 'invalid node cap')
    out = {'schema':'gtf89.quadratic-certificate/1','status':'success',
           'input_sha256':hashlib.sha256(canonical(data).encode()).hexdigest(),
           'witness':budget_witness(data['N'],data['Q']),
           'local_rate_formulas':{'regular':'min(1,s*sqrt(N))',
                                  'coherent':'min(1,s*sqrt(Q))',
                                  'opening':'min(1,s*N)'},
           'scope':'Supremum over the hard-budget reset class; not a lower for each policy.',
           'reset_independence_verified':False,'local_fidelity_coefficient_verified':False,
           'reset_defects_calibrated':False,'operational_distance_computed':False,
           'recovery_synthesized':False,'physical_protocol_executed':False,
           'continuum_proof_by_replay':False,'priority_certified':False}
    require('reset_defects' not in data or 'policy' in data,'defects require a complete policy')
    if 'policy' in data:
        pol = data['policy']
        cert = legacy.analyze(pol, max_nodes=max_nodes)
        require(cert['max_calls'] <= data['N'] and cert['square_cost'] <= data['Q'],
                'policy exceeds requested hard budget')
        out['policy'] = cert
        if 'reset_defects' in data:
            defects=data['reset_defects']; nodes=pol['nodes']
            require(type(defects) is dict and set(defects)==set(nodes),
                    'every formal policy node needs one defect allowance')
            ds={k:legacy.rational(v) for k,v in defects.items()}
            require(all(0 <= v <= 2 for v in ds.values()), 'defects must be in [0,2]')
            require(all(ds[k]==0 for k,n in nodes.items() if not n['children']),
                    'terminal preparation defect must be zero')
            # legacy.analyze already validated acyclicity, reachability and successors.
            done={};stack=[(pol['root'],False)]
            while stack:
                k, expanded=stack.pop()
                if k in done: continue
                children=nodes[k]['children']
                if not expanded:
                    stack.append((k,True));stack.extend((c,False) for c in children)
                else:
                    done[k]=ds[k]+max((done[c] for c in children),default=Fraction(0))
            eps=done[pol['root']]
            out['conditional_reset_defect']={'worst_path_sum':str(eps),
                                            'additive_two_hypothesis_trace_allowance':str(2*eps),
                                            'hypothesis':'Uniform unhalved diamond preparation error at every history, with references.'}
    return out


def verify(data: dict[str, Any], receipt: Any, **kwargs: Any) -> dict[str, Any]:
    expected=analyze(data,**kwargs)
    require(canonical(expected)==canonical(receipt), 'typed exact replay mismatch')
    return expected


def load(path: Path) -> dict[str, Any]:
    raw=path.read_bytes()
    require(len(raw)<=4_000_000, 'input byte cap exceeded')
    return json.loads(raw,object_pairs_hook=legacy.unique_pairs)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--verify',type=Path)
    p.add_argument('--max-nodes',type=int,default=10000);a=p.parse_args()
    try:
        data=load(a.input)
        out=verify(data,load(a.verify),max_nodes=a.max_nodes) if a.verify else analyze(data,max_nodes=a.max_nodes)
        print(json.dumps(out,indent=2,sort_keys=True))
    except (ValueError,TypeError,OSError,KeyError,OverflowError) as e:
        p.exit(2,'rejected: '+str(e)+'\n')


if __name__=='__main__':main()
