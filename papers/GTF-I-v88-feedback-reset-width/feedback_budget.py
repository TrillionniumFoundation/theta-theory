#!/usr/bin/env python3
"""Exact finite public-policy budgets for the reset-protocol fidelity lemma.

The supplied local fidelity majorant is a hypothesis, not verified physical
calibration. This program does not certify reset independence or any device.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def rational(value: Any) -> Fraction:
    require(isinstance(value, str), 'rational values must be canonical strings')
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    require(str(result) == value, 'noncanonical rational')
    return result


def canonical(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def analyze(data: dict, *, max_nodes: int = 10000) -> dict:
    require(type(max_nodes) is int and max_nodes > 0, 'invalid resource cap')
    require(type(data) is dict and set(data) == {'schema','N','b','s','gamma','root','nodes'},
            'unexpected policy fields')
    require(data['schema'] == 'gtf88.reset-policy/1', 'unknown policy schema')
    N,b = data['N'],data['b']
    require(type(N) is int and type(b) is int and 1 <= b <= N, 'invalid call/width budget')
    s,gamma = rational(data['s']),rational(data['gamma'])
    require(s > 0 and gamma >= 0, 'invalid scale or majorant')
    nodes,root = data['nodes'],data['root']
    require(type(nodes) is dict and 0 < len(nodes) <= max_nodes, 'node cap exceeded or empty policy')
    require(all(type(k) is str and k for k in nodes), 'invalid node identity')
    require(type(root) is str and root in nodes, 'missing root')
    active,done,order = set(),{},[]
    stack = [(root,False)]
    while stack:
        name,expanded = stack.pop()
        if name in done:
            continue
        require(name in nodes, 'missing policy child')
        node = nodes[name]
        require(type(node) is dict and set(node) == {'calls','children'}, 'invalid node fields')
        n,children = node['calls'],node['children']
        require(type(n) is int and 0 <= n <= b, 'invalid node call reservation')
        require(type(children) is list and all(type(x) is str and x for x in children), 'invalid children')
        require(len(set(children)) == len(children), 'duplicate outcome branch')
        require((n == 0) == (len(children) == 0), 'nonterminal requires calls and terminal requires none')
        if not expanded:
            require(name not in active, 'cyclic policy')
            active.add(name)
            stack.append((name,True))
            stack.extend((child,False) for child in reversed(children))
            continue
        require(all(child in done for child in children), 'cyclic or incomplete policy')
        if n == 0:
            info = {'max_calls':0,'square_cost':0,'local_product_lower':Fraction(1)}
        else:
            calls = n + max(done[x]['max_calls'] for x in children)
            cost = n*n + max(done[x]['square_cost'] for x in children)
            require(calls <= N, 'pathwise call budget exceeded')
            lower = max(Fraction(0),1-gamma*n*n*s*s)
            lower *= min(done[x]['local_product_lower'] for x in children)
            info = {'max_calls':calls,'square_cost':cost,'local_product_lower':lower}
        done[name] = info
        active.remove(name)
        order.append(name)
    require(set(done) == set(nodes), 'unreachable or unverified policy nodes')
    result = done[root]
    Q = result['square_cost']
    additive = max(Fraction(0),1-gamma*Q*s*s)
    require(result['local_product_lower'] >= additive, 'fidelity recursion failed')
    require(Q <= b*result['max_calls'], 'integer width identity failed')
    return {
        'schema':'gtf88.reset-budget/1','status':'success',
        'policy_sha256':hashlib.sha256(canonical(data)).hexdigest(),
        'nodes':len(nodes),'max_calls':result['max_calls'],'square_cost':Q,'width_cap':b,
        'conditional_root_fidelity_lower':str(additive),
        'conditional_product_lower':str(result['local_product_lower']),
        'conditional_trace_bound_squared':str(min(Fraction(4),8*gamma*Q*s*s)),
        'all_reachable_nodes_checked':True,
        'local_fidelity_majorant_verified':False,
        'physical_reset_independence_verified':False,
        'exact_operational_distance_computed':False,
        'physical_protocol_executed':False,
        'continuum_proof_by_replay':False,
        'qualification':'Conditional budget consequences only; local fidelity and reset are hypotheses.'
    }


def unique_pairs(pairs):
    out = {}
    for key,value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique_pairs)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('policy',type=Path)
    parser.add_argument('--verify',type=Path)
    parser.add_argument('--max-nodes',type=int,default=10000)
    args=parser.parse_args()
    try:
        result=analyze(load(args.policy),max_nodes=args.max_nodes)
        if args.verify:
            require(load(args.verify) == result,'certificate replay mismatch')
        print(json.dumps(result,sort_keys=True,indent=2))
    except (ValueError,OSError,TypeError) as exc:
        parser.exit(2,'rejected: '+str(exc)+'\n')

if __name__ == '__main__':
    main()
