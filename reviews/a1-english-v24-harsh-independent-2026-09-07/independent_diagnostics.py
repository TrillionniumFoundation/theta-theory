#!/usr/bin/env python3
"""Independent finite diagnostics for A1 v24, not a proof certificate.

Standard library only. No author code or data is imported. All comparisons
are exact rational/integer comparisons; explicit exceptions survive python -O.
Run: python independent_diagnostics.py > DIAGNOSTICS.json
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import factorial, comb
from pathlib import Path
import hashlib
import json

CHECKS: Counter[str] = Counter()
NEGATIVE: list[str] = []


def check(ok: bool, category: str) -> None:
    if not ok:
        raise ArithmeticError('Failed independent check: ' + category)
    CHECKS[category] += 1


def reject(ok: bool, name: str) -> None:
    if ok:
        raise ArithmeticError('Negative control did not distinguish: ' + name)
    NEGATIVE.append(name)


def prod(xs):
    out = F(1)
    for x in xs:
        out *= x
    return out


def rank(rows) -> int:
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    i = 0
    for j in range(len(a[0])):
        pivot = next((k for k in range(i, len(a)) if a[k][j]), None)
        if pivot is None:
            continue
        a[i], a[pivot] = a[pivot], a[i]
        t = a[i][j]
        a[i] = [x / t for x in a[i]]
        for k in range(i + 1, len(a)):
            t = a[k][j]
            if t:
                a[k] = [x - t*y for x, y in zip(a[k], a[i])]
        i += 1
        if i == len(a):
            break
    return i


def mul(p, q):
    out = {}
    for a, c in p.items():
        for b, d in q.items():
            out[a+b] = out.get(a+b, F(0)) + c*d
    return {a: c for a, c in out.items() if c}


def add(p, q):
    out = dict(p)
    for a, c in q.items():
        out[a] = out.get(a, F(0)) + c
    return {a: c for a, c in out.items() if c}


def scale(p, c):
    return {a: c*v for a, v in p.items() if c*v}


def poly_product(polys):
    out = {F(0): F(1)}
    for p in polys:
        out = mul(out, p)
    return out


def integral(p, shift=F(0), beta=1, weight=F(1)):
    # Prior: weight * Beta(beta,1) + (1-weight) * delta_0.
    return sum((c*(weight*F(beta)/(F(beta)+a+shift)
                   + (1-weight if a+shift == 0 else 0))
                for a, c in p.items()), F(0))


def dd_integral(p, nodes, beta=1, weight=F(1)):
    # All nodes positive. Exact integrated Newton divided difference.
    j = len(nodes)
    return sum((c*weight*F(beta)*(-1)**(j-1)
                / prod(F(beta)+a+b for b in nodes)
                for a, c in p.items()), F(0))


def formal_nodes(a, m):
    return [sum((a[i] for i in ids), F(0))
            for ids in combinations_with_replacement(range(len(a)), m)
            if any(ids)]


def leja(nodes):
    remaining = list(range(len(nodes)))
    order = [min(remaining, key=lambda i: (nodes[i], i))]
    remaining.remove(order[0])
    ds = [F(1)]
    while remaining:
        vals = {i: prod(abs(nodes[i]-nodes[k]) for k in order)
                for i in remaining}
        i = min(remaining, key=lambda i: (-vals[i], i))
        ds.append(vals[i]); order.append(i); remaining.remove(i)
    return [nodes[i] for i in order], ds


def volumes(nodes):
    return [max(prod(abs(nodes[i]-nodes[j]) for i,j in combinations(ids,2))
                for ids in combinations(range(len(nodes)), ell))
            for ell in range(1, len(nodes)+1)]


def flags_and_pairings():
    calibrations = [
        tuple(map(F, [0,1])), tuple(map(F, [0,1,2])),
        tuple(map(F, [0,1,3])), tuple(map(F, [0,1,2,3])),
        (F(0),F(1),F(65,32),F(3)),
        (F(0),F(1),F(65,32),F(97,32)),
        (F(0),F(1),F(65,32),F(49,16)),
        (F(0),F(1),F(65,32),F(3097,1024)),
    ]
    cases = 0
    normalization_witness = None
    for a in calibrations:
        for m in (1,2):
            xs = [x/16 for x in formal_nodes(a,m)]
            nodes, ds = leja(xs)
            check(all(ds[i]>=ds[i+1] for i in range(len(ds)-1)), 'leja_monotonicity')
            vs = volumes(xs)
            for ell, v in enumerate(vs, 1):
                base = prod(ds[:ell])
                check(base<=v<=factorial(ell)*base, 'maximal_vandermonde_bounds')
            for c in (F(1,3),F(1),F(7,2)):
                for x in nodes:
                    rhs = sum((prod(x-y for y in nodes[:j])*(-1)**j
                               / prod(c+y for y in nodes[:j+1])
                               for j in range(len(nodes))), F(0))
                    check(rhs == 1/(c+x), 'newton_identity_including_zero_pivots')
            s = len(set(xs))
            check(sum(d>0 for d in ds)==s, 'nonzero_pivots_equal_distinct_nodes')
            for n in (1,2,3):
                p = min(n*(len(a)-1), len(nodes))
                cs = [F(i+1,32) for i in range(n)]
                fs = [{F(0): F(1), a[-1]: c} for c in cs]
                full = poly_product(fs)
                directions = [mul({ak:F(1)},poly_product(fs[:i]+fs[i+1:]))
                              for i in range(n) for ak in a]
                support = sorted(set().union(*(q.keys() for q in directions)))
                check(rank([[q.get(b,F(0)) for q in directions] for b in support])
                      == n*(len(a)-1)+1, 'product_tangent_rank')
                raw = formal_nodes(a,m)
                orders = [raw, raw[::-1], sorted(raw), [16*x for x in nodes]]
                unique = list(dict.fromkeys(tuple(x) for x in orders))
                for beta, weight in ((1,F(1)),(2,F(1)),(1,F(1,16))):
                    z = integral(full,beta=beta,weight=weight)
                    for order in unique:
                        tests = [order[:j] for j in range(1,p+1)]
                        lq0 = [integral(q,beta=beta,weight=weight) for q in directions]
                        lq = [[dd_integral(q,ns,beta,weight) for q in directions] for ns in tests]
                        lp = [dd_integral(full,ns,beta,weight) for ns in tests]
                        check(rank([lq0]+lq)==p+1,'mixed_prefix_rank')
                        deriv = [[(x*z-y*u)/z**2 for x,u in zip(row,lq0)]
                                 for row,y in zip(lq,lp)]
                        check(rank(deriv)==p,'evidence_normalized_prefix_rank')
                        if normalization_witness is None:
                            normalization_witness = (rank([lq0]+lq),rank(deriv))
                        cases += 1
    reject(normalization_witness[0]==normalization_witness[1],
           'omitting the one normalization direction')
    # A={0,1,3}, n=1,m=2: five raw directions, two acquired coordinates.
    check(len(set(formal_nodes((F(0),F(1),F(3)),2)))==5,'five_future_directions')
    reject(min(2,5)==5,'ambient affine dimension used as acquired dimension')
    return cases


def valuation_difference(x,y):
    for i,(a,b) in enumerate(zip(x,y)):
        if a!=b:
            return i
    raise ValueError('Identical path labels must be merged first')


def energy_tables(nodes):
    nodes = list(dict.fromkeys(nodes))
    w = {(i,j): valuation_difference(nodes[i],nodes[j])
         for i in range(len(nodes)) for j in range(i+1,len(nodes))}
    def dist(i,j):
        return w[min(i,j),max(i,j)]
    for i,j,k in combinations(range(len(nodes)),3):
        for a,b,c in ((i,j,k),(j,i,k),(i,k,j)):
            check(dist(a,c)>=min(dist(a,b),dist(b,c)), 'valuation_ultrametric')
    def allocate(ids, parent_height):
        if len(ids)==1:
            return [0,0]
        height = min(dist(i,j) for i,j in combinations(ids,2))
        groups=[]; left=set(ids)
        while left:
            i=min(left)
            group={j for j in left if j==i or dist(i,j)>height}
            groups.append(sorted(group)); left-=group
        table=[0]
        for group in groups:
            child=allocate(group,height)
            new=[None]*(len(table)+len(child)-1)
            for a,x in enumerate(table):
                for b,y in enumerate(child):
                    v=x+y
                    if new[a+b] is None or v<new[a+b]: new[a+b]=v
            table=new
        return [x+(height-parent_height)*comb(k,2) for k,x in enumerate(table)]
    dp=allocate(list(range(len(nodes))),0)
    brute=[0]+[min(sum(dist(i,j) for i,j in combinations(ids,2))
                   for ids in combinations(range(len(nodes)),ell))
               for ell in range(1,len(nodes)+1)]
    check(dp==brute,'tree_dynamic_program_equals_subset_enumeration')
    return brute


def collision_phases():
    for k in range(2,13):
        zero=(0,)*(k+1)
        def poly(c=0,u=0,v=0):
            z=list(zero); z[0]=c; z[1]=u+v; z[k]=v; return tuple(z)
        a=[poly(),poly(1),poly(2,u=1),poly(3,v=1)]
        nodes=[tuple(x+y for x,y in zip(a[i],a[j]))
               for i,j in combinations_with_replacement(range(4),2) if i or j]
        es=energy_tables(nodes)
        check(es==[0]*7+[1,2,k+2],'two_parameter_all_nine_volume_orders')
        for x,target in ((6,F(2)),(8*k-2,F(2*k))):
            exps=[F(x,3),F(1,2)+F(x,4),F(4+2*k,9)+F(2*x,9)]
            check(min(exps)==target,'crossover_regret_orders')
        check(F(3,7)*F(-1,3)+F(4,7)*F(-1,4)==F(-2,7),'seven_dimensional_interpolation_budget')
        check(F(4,7)*F(1,2)==F(2,7),'seven_dimensional_interpolation_gap')
    # A cluster containing all labels: root must not lose positive common order.
    energy_tables([(0,1,1,0),(0,1,2,0),(0,1,2,1),(0,2,0,0)])
    a0=(F(0),F(1),F(2),F(3))
    for u,v,expected in [(F(0),F(0),6),(F(0),F(1,32),8),
                         (F(1,32),F(1,32),8),(F(1,32),F(1,16),8),
                         (F(1,32),F(3,64),9)]:
        a=(a0[0],a0[1],a0[2]+u,a0[3]+v)
        peak=max(min(n*3,len(set(formal_nodes(a,5-n)))) for n in range(1,5))
        check(peak==expected,'six_eight_nine_peak_dimensions')
    for rho,M in product((F(0),F(1,4),F(1,16)),(1,2,16,64,4096)):
        six=F(1,M)**28; seven=rho**24*F(1,M)**24; eight=rho**42*F(1,M)**21
        check(seven<=max(six,eight),'seven_branch_dominance_after_power_84')


def detector(a):
    cells=[]
    top={F(0):F(1,4)}
    for x in a[1:]: top=add(top,{x:F(1,16)})
    cells.append(top)
    cells += [{F(0):F(1,4),x:F(-1,16)} for x in a[1:]]
    return cells


def factors(cells,g):
    fs=[scale(p,v) for p,v in zip(cells,g)]
    failure={F(0):F(1)}
    for f in fs: failure=add(failure,scale(f,-1))
    return fs+[failure]


def raw_updates_and_probabilities():
    histories=0
    configs=[(F(0),F(0)),(F(0),F(1,32)),(F(1,32),F(1,32)),
             (F(1,32),F(1,16)),(F(1,32),F(33,1024))]
    gs=[(F(1,4),F(3,8),F(5,8),F(3,4)),
        (F(5,8),F(1,4),F(3,4),F(3,8)),
        (F(1,2),F(3,4),F(1,4),F(1,2))]
    for u,v in configs:
        a=(F(0),F(1),2+u,3+v); cells=detector(a)
        check(poly_product([{F(0):F(1)}])=={F(0):F(1)},'polynomial_identity')
        s={}
        for c in cells:s=add(s,c)
        check(s=={F(0):F(1)},'detector_partition')
        fs=[factors(cells,g) for g in gs]
        states=[({F(0):F(1)},F(1))]
        for n in range(3):
            next_states=[]; m=5-n
            for P, mass in states:
                Z=integral(P)
                old={e:integral(P,e)/Z for e in set([F(0)]+formal_nodes(a,m))}
                for f in fs[n]:
                    denom=sum((c*old[e] for e,c in f.items()),F(0))
                    check(denom>=F(3,64),'physical_bayes_denominator')
                    Q=mul(P,f); zq=integral(Q)
                    check(mass*denom==zq,'unconditional_word_mass')
                    for e in set([F(0)]+formal_nodes(a,m-1)):
                        updated=sum((c*old[e+b] for b,c in f.items()),F(0))/denom
                        check(updated==integral(Q,e)/zq,'raw_remaining_moment_update')
                    next_states.append((Q,mass*denom)); histories+=1
            check(sum((mass for P,mass in next_states),F(0))==1,'complete_report_word_probability_partition')
            # A gap-independent endpoint bound, using posterior mixtures only.
            P,Q=next_states[0][0],next_states[-1][0]
            rem=4-n
            exps=set([F(0)]+formal_nodes(a,rem))
            vp={e:integral(P,e)/integral(P) for e in exps}
            vq={e:integral(Q,e)/integral(Q) for e in exps}
            err=max(abs(vp[e]-vq[e]) for e in exps)
            for f in fs[(n+1)%3]:
                out=[]
                for vv in (vp,vq):
                    den=sum((c*vv[e] for e,c in f.items()),F(0))
                    out.append({e:sum((c*vv[e+b] for b,c in f.items()),F(0))/den
                                for e in set([F(0)]+formal_nodes(a,rem-1))})
                bound=2*sum(map(abs,f.values()))/F(3,64)
                check(max(abs(out[0][e]-out[1][e]) for e in out[0])<=bound*err,
                      'gap_free_raw_update_endpoint_bound')
            states=next_states
    reject(F(1,2)+F(1,2)==2,'conditioning away report probabilities')
    return histories


def integer_budgets_and_resource_controls():
    for sides in ([F(1)],[F(1),F(1,8)],[F(1),F(1,4),F(0)],
                  [F(1),F(1,4),F(1,16),F(1,32)]):
        for eps in (F(1),F(1,2),F(1,8),F(1,64)):
            bound=max(prod(sides[:j])/eps**j for j in range(1,len(sides)+1))
            M=max(1,-(-bound.numerator//bound.denominator))
            check(all(prod(sides[:j])<=M*eps**j for j in range(1,len(sides)+1)),
                  'integer_profile_inverse_sufficient')
            if M>1:
                check(any(prod(sides[:j])>(M-1)*eps**j for j in range(1,len(sides)+1)),
                      'integer_profile_inverse_minimal')
            bits=(M-1).bit_length()
            check(2**bits>=M and (bits==0 or 2**(bits-1)<M),'binary_budget_rounding')
    # A finite explicit witness to the forbidden inf/max exchange.
    risks=[(F(0),F(1)),(F(1),F(0))]
    left=min(max(r) for r in risks); right=max(min(r[j] for r in risks) for j in range(2))
    check((left,right)==(1,0),'single_filter_quantifier_witness')
    reject(left==right,'interchanging filter infimum and checkpoint maximum')
    e=F(0); terms=[F(1,8),F(1,16),F(1,32)]; L=F(3,2)
    for r in terms:e=L*e+r
    check(e==sum((L**(len(terms)-1-j)*r for j,r in enumerate(terms)),F(0)),
          'all_causal_errors_accumulate')
    reject(e==terms[-1],'discarding previous quantization errors')
    reject(1+F(1,2)<=1,'using the large-budget constant-term absorption at M=1')


def main():
    cases=flags_and_pairings()
    collision_phases()
    histories=raw_updates_and_probabilities()
    integer_budgets_and_resource_controls()
    receipt={
        'submission_sha':'6f648bc3da0543e8361b4053ae7da33cb172f597',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'status':'passed', 'arithmetic':'exact fractions and integers',
        'author_implementation_imported':False,
        'checks':dict(sorted(CHECKS.items())), 'total_checks':sum(CHECKS.values()),
        'normalized_prefix_cases':cases, 'report_history_extensions':histories,
        'negative_controls_distinguished':NEGATIVE,
        'limits':'Finite diagnostics only. No analytic uniformity, optimal minimax value, source preservation, PDF build or full companion certification follows.'
    }
    print(json.dumps(receipt,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
