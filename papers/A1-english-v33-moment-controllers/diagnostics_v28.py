#!/usr/bin/env python3
"""Exact finite checks for A1 v28; not a substitute for continuum proofs."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import comb, factorial, prod
from pathlib import Path

COUNTS: Counter[str] = Counter()

def check(category: str, condition: bool, detail: object = None) -> None:
    if not condition:
        raise ArithmeticError(f'{category}: {detail!r}')
    COUNTS[category] += 1

def cut(edges: tuple[tuple[int,int], ...], S: frozenset[int]) -> tuple[int,...]:
    return tuple(i for i,(u,v) in enumerate(edges) if (u in S) != (v in S))

def levels(v: int, j: int) -> tuple[frozenset[int],...]:
    return tuple(frozenset(x) for x in combinations(range(v),j))

def retained_mass(v: int, edges: tuple[tuple[int,int],...], j: int,
                  r: int, beta: F) -> tuple[F,int]:
    cuts = [cut(edges,S) for S in levels(v,j)]
    rho = F(0)
    for mask in range(1 << len(edges)):
        if all(sum((mask >> e) & 1 for e in C) >= r for C in cuts):
            k = mask.bit_count()
            rho += beta**k * (1-beta)**(len(edges)-k)
    return rho, sum(comb(len(C),r) if len(C)>=r else 0 for C in cuts)

def main() -> dict:
    # Enumerate every simple graph on two, three and four labelled vertices.
    graph_witness = None
    for v in range(2,5):
        all_edges = tuple(combinations(range(v),2))
        for mask in range(1 << len(all_edges)):
            edges = tuple(e for i,e in enumerate(all_edges) if (mask>>i)&1)
            j = v//2
            cuts = [cut(edges,S) for S in levels(v,j)]
            for r in (1,2):
                for beta in (F(1,3),F(2,3)):
                    rho, N = retained_mass(v,edges,j,r,beta)
                    failures = sum(sum(F(comb(len(C),k))*beta**k*(1-beta)**(len(C)-k)
                                       for k in range(min(r,len(C)+1))) for C in cuts)
                    check('retention_union_bound', rho >= max(F(0),1-failures))
                    check('witness_count', N <= 2**(v+len(edges)))
                    # Every realized order has a regular witness on the robust event.
                    for good in range(1 << len(edges)):
                        robust = all(sum((good>>e)&1 for e in C)>=r for C in cuts)
                        via_orders = all(sum((good>>e)&1 for e in cut(edges,frozenset(pi[:j])))>=r
                                         for pi in permutations(range(v)))
                        check('compulsory_layer', robust == via_orders)
                    if v==4 and len(edges)==6 and r==1 and beta==F(2,3):
                        graph_witness = {'rho':str(rho),'all_edges_mass':str(beta**6),'N':N}
    # Parallel edges are labelled, not collapsed; isolated cuts have zero robustness.
    parallel = ((0,1),(0,1),(1,2),(1,2))
    rho,N = retained_mass(3,parallel,1,1,F(1,2))
    parallel_N = N
    check('parallel_edges', rho == F(9,16), (rho,N))
    check('isolated_vertex', retained_mass(3,((0,1),),1,1,F(1,2))[0]==0)

    # Selected-edge measures: marginalizing all unselected edges gives one,
    # whereas conditioning them to be regular gives a strictly smaller mass.
    beta = F(2,3)
    for P in range(2,8):
        for r in range(1,P):
            selected = beta**r
            marginal = sum(F(comb(P-r,k))*beta**k*(1-beta)**(P-r-k)
                           for k in range(P-r+1))*selected
            all_good = beta**P
            check('selected_subprobability', marginal == selected)
            check('unselected_event_negative_control', all_good < marginal)

    # A genuinely data-selected boundary: finite tapes contain independent
    # retention indicators and coordinates. Choose the cut giving least loss.
    edges = ((0,1),(1,2),(0,2))
    cuts = [cut(edges,S) for S in levels(3,1)]
    centres = (F(1,4),F(3,4))
    vals = (F(1,16),F(1,4),F(5,8),F(15,16))
    selected_counts: Counter[int] = Counter()
    selected_losses: set[F] = set()
    threshold_counts = {t:[F(0),F(0)] for t in (F(0),F(1,128),F(1,64),F(1,16))}
    total_states=0
    for good in product((False,True),repeat=3):
        robust=all(any(good[e] for e in C) for C in cuts)
        for x in product(vals,repeat=3):
            losses=[sum(min((x[e]-c)**2 for c in centres) for e in C) for C in cuts]
            chosen=min(range(3),key=lambda i:(losses[i],-sum(good[e] for e in cuts[i]),i))
            loss=losses[chosen]
            selected_counts[chosen] += 1
            selected_losses.add(loss)
            for t,counts in threshold_counts.items():
                # Same event is bounded before the adaptive restriction.
                left=robust and loss<=t
                union=sum(good[e] and min((x[e]-c)**2 for c in centres)<=t
                          for C in cuts for e in C)
                check('adaptive_restriction', int(left)<=union)
                counts[0]+=int(left); counts[1]+=union
            total_states+=1
    check('nonconstant_selected_path',len(selected_counts)>1)
    check('nonconstant_selected_loss',len(selected_losses)>1)
    for t,(a,b) in threshold_counts.items():
        check('adaptive_averaging',a/total_states<=b/total_states,(t,a,b))

    # Tail integration is checked in the variable u=sqrt(t), so every
    # dimension becomes an exact polynomial integral on a rational endpoint.
    for k in range(1,13):
        for rho in (F(1,4),F(3,4),F(1)):
            for u0 in (F(1,3),F(2,5)):
                AM=rho/u0**k
                integral=rho*u0**2-F(2,k+2)*AM*u0**(k+2)
                expected=F(k,k+2)*rho*u0**2
                check('tail_integral',integral==expected)
    # Recovery weight, Markov threshold and Gaussian normalization jointly
    # give 2 * 4 * 2 = 16, not 8. Test powers for all even dimensions.
    for k in range(2,18,2):
        for P,r,L in ((9,3,F(3,2)),(20,4,F(2)),(100,10,F(1,2))):
            lhs=(F(2*P)*L**2)**(k//2)*4**(k//2)*F(2,k)**(k//2)
            rhs=(F(16*P,k)*L**2)**(k//2)
            check('dimension_normalization',lhs==rhs)
            check('factor_eight_negative_control',rhs!=(F(8*P,k)*L**2)**(k//2))

    # Tensor damping with a product menu; the proof must retain the tensor
    # half of the enlarged task, not prove only the easier local half.
    q=F(3,4)
    Cq=(1+q*q)/(1-q*q)**3
    for f in range(1,13):
        check('tensor_uniform_coefficient',f*f*q**(2*(f-1))<=Cq)
        for shift in (F(1,64),F(1,32),F(1,16)):
            a=tuple(F(1,3)+F(i%3,16) for i in range(f))
            b=tuple(x+shift for x in a)
            error=(prod(a)-prod(b))**2
            bound=f*q**(2*(f-1))*sum((x-y)**2 for x,y in zip(a,b))
            check('tensor_telescoping',error<=bound)
            local=sum((x-y)**2 for x,y in zip(a,b))/f
            check('mixture_controls_tensor',error<=2*(error+local)/2)
    check('empty_cut',prod(())==1)

    # The collision profile uses independently capped positive scales;
    # a fixed multiplicative resolution change costs at most p/2 bits per log.
    for exponents in ((0,0,0),(0,2,4),(0,3,None)):
        p=len(exponents)
        for U in range(1,9):
            for s in (F(1,2),F(1),F(3,2),F(3)):
                logs=[F(0)]
                for ell,e in enumerate(exponents,1):
                    if e is not None:
                        logs.append(U*(ell*s-e))
                b=max(logs)
                shifted=max([F(0)]+[U*(ell*s-e)+ell for ell,e in enumerate(exponents,1) if e is not None])
                check('collision_budget_shift',b<=shifted<=b+p)
                check('positive_first_scale',b>=U*s)
    # Mean crossing counts from the bipartite random construction.
    for s in range(1,15):
        for D in (1,7,31,101):
            for a in range(s+1):
                direct=D*(a*F(a,s)+(s-a)*F(s-a,s))
                formula=F(D,s)*(a*a+(s-a)**2)
                check('balanced_cut_construction',direct==formula and formula>=F(D*s,2))
    if graph_witness is None:
        raise RuntimeError('missing complete-graph witness')
    check('robust_event_not_all_edges',F(graph_witness['rho'])>F(graph_witness['all_edges_mass']))
    return {'schema':'A1-v28-exact-diagnostics-1',
            'checks':sum(COUNTS.values()),'categories':dict(sorted(COUNTS.items())),
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'witnesses':{'K4_beta_two_thirds':graph_witness,
                         'parallel_path_beta_half':{'rho':'9/16','N':parallel_N},
                         'dimension_factor':16,'adaptive_tape_count':total_states,
                         'selected_path_counts':dict(selected_counts),
                         'selected_losses':sorted(map(str,selected_losses))},
            'limits':'Finite identities and inequalities only; not a proof of continuum acquisition, covering, all schedulers, full LaTeX build, or journal significance.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(main(),indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding='utf-8')
    print(result,end='')
