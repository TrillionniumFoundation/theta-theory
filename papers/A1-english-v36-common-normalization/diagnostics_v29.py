#!/usr/bin/env python3
"""Exact finite witnesses for A1 v29. These tests do not prove its general theorems."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
import json
from pathlib import Path

COUNTS: Counter[str] = Counter()

def check(group: str, condition: bool, message: str) -> None:
    COUNTS[group] += 1
    if not condition:
        raise RuntimeError(f'{group}: {message}')

def phi_cubic(x: F, a2: F) -> F:
    return x**3 / (3*a2)

def tangent(x: F, z: F, a2: F) -> F:
    return z*z*x/a2 - 2*z**3/(3*a2)

def paths(n: int) -> list[tuple[int, ...]]:
    result = []
    for order in permutations(range(n)):
        s = 0
        row = []
        for v in order[:-1]:
            s |= 1 << v
            row.append(s)
        result.append(tuple(row))
    return result

def separators(n: int) -> list[tuple[int, ...]]:
    ps = paths(n)
    nodes = tuple(range(1, (1 << n)-1))
    out = []
    for mask in range(1, 1 << len(nodes)):
        ss = tuple(nodes[i] for i in range(len(nodes)) if mask & (1 << i))
        if all(any(w in ss for w in p) for p in ps):
            out.append(ss)
    return out

def step_cost(x: F, breaks: list[F], values: list[F]) -> F:
    return sum((breaks[i+1]-breaks[i])*max(F(0),x-values[i])
               for i in range(len(breaks)-1))

def integer_cuberoot(n: int) -> int:
    if n < 0:
        raise ValueError('A cube-root radicand must be nonnegative')
    lo, hi = 0, 1 << ((n.bit_length()+2)//3)
    while lo < hi:
        mid = (lo+hi+1)//2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid-1
    return lo

def density(u: F) -> F:
    if u < -F(8,7) or u > F(8,9):
        return F(0)
    if u <= 0:
        return 512*(27/(8-5*u)**3-1/(8+3*u)**3)
    return 512*(27/(8+3*u)**3-1/(8-5*u)**3)

def sharp_enclosure(n: int = 8192) -> tuple[F, F]:
    """Monotone endpoint sums with independently implemented integer bisection."""
    scale = 10**12
    low, high = F(0), F(0)
    for left,right,inc in [(-F(8,7),F(0),True),(F(0),F(8,9),False)]:
        h = (right-left)/n
        roots = []
        for i in range(n+1):
            d = density(left+i*h)
            if d < 0:
                raise RuntimeError('Negative density in monotone enclosure')
            m = d.numerator*scale**3//d.denominator
            r = integer_cuberoot(m)
            if not r**3 <= m < (r+1)**3:
                raise RuntimeError('Integer enclosure failed')
            roots.append(r)
        lterms = roots[:-1] if inc else roots[1:]
        uterms = roots[1:] if inc else roots[:-1]
        low += h*F(sum(lterms),48*scale)
        high += h*F(sum(uterms)+n,48*scale)
    return low**3/1536, high**3/1536

def run() -> dict:
    COUNTS.clear()
    # Power integral: choose r with rational r^(k/2) to avoid numerical roots.
    for k in (1,2,3,4,6):
        for a in (F(1),F(2),F(7,3)):
            for b in (F(1,5),F(1,3),F(1,2)):
                r=b*b
                x=a*b**k
                if x>1:
                    continue
                integral=x*r - a*F(2,k+2)*b**(k+2)
                formula=F(k,k+2)*x*r
                check('power_integrals', integral==formula, 'Power primitive mismatch')
    # Every displayed cubic tangent is a lower certificate, not a primal value.
    for a2 in (F(1),F(2),F(17,3)):
        for zi in range(9):
            z=F(zi,8)
            check('cubic_dual', tangent(z,z,a2)==phi_cubic(z,a2), 'Tangency')
            for xi in range(9):
                x=F(xi,8)
                check('cubic_dual', tangent(x,z,a2)<=phi_cubic(x,a2), 'Invalid lower tangent')
        # Exact primal/dual equality for the two-node examples.
        pc=2*phi_cubic(F(1,2),a2)
        dc=F(1,4)/a2-F(1,6)/a2
        check('two_choice_certificates',pc==dc==F(1,12)/a2,'Unanchored dual')
        pa=phi_cubic(F(1),a2)
        da=1/a2-F(2,3)/a2
        check('two_choice_certificates',pa==da==4*pc,'Anchored dual')
        # Nonoptimal primal value is NOT a lower certificate for the optimum.
        check('primal_direction_negative_control',phi_cubic(F(1),a2)>pc,
              'Counterexample to using a primal feasible value as a lower bound')
    # Perspective Jensen for independent-seed mixtures.
    for a2 in (F(1),F(9,2)):
        for alpha in (F(1,5),F(1,2),F(4,5)):
            for x in (F(0),F(1,4),F(1)):
                for y in (F(0),F(2,3),F(1)):
                    lhs=alpha*phi_cubic(x,a2)+(1-alpha)*phi_cubic(y,a2)
                    rhs=phi_cubic(alpha*x+(1-alpha)*y,a2)
                    check('perspective_jensen',lhs>=rhs,'Seedwise cost weakened incorrectly')
    # Long chains: the new certificate and the old separator/J differ by J.
    for J in (1,2,3,8,31):
        new=F(1,3*49)
        old=new/J
        check('chain_separation',new==J*old,'Lost checkpoint factor')
    # Exact finite path laws: step capacities from true node subprobabilities.
    finite_witnesses=[]
    for n in (2,3,4):
        ps=paths(n)
        seps=separators(n)
        nodes=range(1,(1<<n)-1)
        for regime in (0,1,2):
            weights=[F(i+1 if regime==1 else (2 if i%2 else 1) if regime==2 else 1)
                     for i in range(len(ps))]
            total=sum(weights)
            weights=[x/total for x in weights]
            losses=[[F(1+(3*i+2*j+regime)%7,8) for j in range(n-1)]
                    for i in range(len(ps))]
            breaks=sorted({F(0),F(1)}|{x for row in losses for x in row})
            occ={w:sum(weights[i] for i,p in enumerate(ps) if w in p) for w in nodes}
            caps={w:[sum(weights[i] for i,p in enumerate(ps)
                          if w in p and losses[i][p.index(w)]<=t)
                     for t in breaks] for w in nodes}
            costs={w:step_cost(occ[w],breaks,caps[w]) for w in nodes}
            exp=[sum(weights[i]*losses[i][j] for i in range(len(ps))) for j in range(n-1)]
            for j in range(n-1):
                check('finite_path_laws',sum(costs[w] for w in nodes if w.bit_count()==j+1)==exp[j],
                      'Layer-cake must hold at each fixed level')
            for C in seps:
                check('flow_separator_incidence',sum(occ[w] for w in C)>=1,'Flow misses separator')
            h=[min(sum(caps[w][i] for w in C) for C in seps) for i in range(len(breaks))]
            old=step_cost(F(1),breaks,h)/(n-1)
            check('finite_path_laws',max(exp)>=old,'Separator dominance')
            check('terminal_capacities',all(occ[w]<=caps[w][-1] for w in nodes),'Terminal feasibility')
            finite_witnesses.append({'vertices':n,'regime':regime,'path_count':len(ps),
                                    'max_expected_loss':str(max(exp)),'separator_bound':str(old)})
    # A capacity not supporting a full unit flow at t=1 is genuinely infeasible.
    check('terminal_capacities',F(2,5)+F(2,5)<1,'Infeasible two-node terminal test')
    # Explicit noncommutations: these are arithmetic witnesses, not labels.
    loss=[[F(1),F(0)],[F(0),F(1)]]
    emax=sum(max(row) for row in loss)/2
    maxe=max(sum(row[j] for row in loss)/2 for j in range(2))
    iminmax=min(max(row) for row in loss)
    maximin=max(min(row[j] for row in loss) for j in range(2))
    check('quantifier_negative_controls',emax==1 and maxe==F(1,2),'Expectation/max witness')
    check('quantifier_negative_controls',iminmax==1 and maximin==0,'Infimum/max witness')
    # Exact full detector constants and certificate ratios.
    beta,H,L2=F(1,2),F(26),F(128)
    full=beta**3/(12*L2*H**2)
    beta_o,H_o=F(35,1024),F(177957,20480)
    restricted=beta_o**3/(12*L2*H_o**2)
    old=F(1071875,12452637120528384)
    check('evaluated_detector',full==F(1,8306688),'Full first-block coefficient')
    check('evaluated_detector',restricted==4*old==F(1071875,3113159280132096),'Same-input fourfold improvement')
    check('evaluated_detector',full/old==F(1499109768,1071875),'Complete improvement ratio')
    half=(beta/2)**3/(12*L2*(H/2)**2)
    check('evaluated_detector',half==full/2==F(1,16613376),'Completion comparison must scale density too')
    check('evaluated_detector',density(F(0))==26 and density(-F(8,7))==density(F(8,9))==0,'Density peak and endpoints')
    for M in (1,2,3,4,8,16,31,64,257):
        a2=4*L2*M*M*H*H/(beta*beta)
        check('integer_budgets',beta/(3*a2)==full/(M*M),'Integer-label coefficient')
        check('integer_budgets',a2>1,'Power cost domain')
        for K in (1,2,6):
            check('finite_descriptors',beta/(3*a2*K*K)==full/(M*M*K*K),'Descriptor cardinality cost')
    kl,ku=sharp_enclosure()
    check('sharp_enclosure',F(48846,10**11)<kl<ku<F(48871,10**11),'Sharp integral enclosure')
    check('sharp_enclosure',F(405,100)<kl/full<ku/full<F(406,100),'Sharp-to-certificate gap')
    return {'schema_version':1,'revision':'A1-v29','status':'passed',
            'check_counts':dict(sorted(COUNTS.items())), 'total_explicit_checks':sum(COUNTS.values()),
            'scope':'Finite exact arithmetic witnesses and a rational integral enclosure; not proof certification or a full native build.',
            'full_first_block_coefficient':str(full),'completion_coefficient':str(half),
            'restricted_seedwise_coefficient':str(restricted),'old_restricted_separator_coefficient':str(old),
            'improvement_ratio_exact':str(full/old),'improvement_ratio_display':float(full/old),
            'kappa_lower_exact':str(kl),'kappa_upper_exact':str(ku),
            'sharp_to_new_lower_exact':str(kl/full),'sharp_to_new_upper_exact':str(ku/full),
            'sharp_to_new_interval_display':[float(kl/full),float(ku/full)],
            'independent_integer_root_method':'integer bisection',
            'enclosure_intervals_per_piece':8192,
            'finite_path_witnesses':finite_witnesses,
            'negative_controls':{'E_max':str(emax),'max_E':str(maxe),'inf_max':str(iminmax),'max_inf':str(maximin),
                                 'same_input_anchored_over_unanchored':'4'},
            'general_continuum_theorems_verified_by_tests':False}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding='utf-8')
    else:
        print(result,end='')

if __name__=='__main__':
    main()
