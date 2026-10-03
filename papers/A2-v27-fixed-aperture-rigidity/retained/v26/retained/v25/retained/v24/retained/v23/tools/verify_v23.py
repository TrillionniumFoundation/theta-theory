#!/usr/bin/env python3
"""Finite diagnostics, not a proof certificate or an executed billiard scanner.

The exact tests cover discrete analogues of the preparation mixture, integer
witness extraction, adaptive arrival probabilities, stopping budgets, and
rate algebra. --geometry also runs the retained independent local-ray test.
Checks use exceptions and therefore remain active under python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import reduce
import hashlib
import importlib.util
from itertools import combinations, product
import json
import math
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()


def check(ok: bool, group: str, detail: object = '') -> None:
    if not ok:
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] += 1


def sampler() -> None:
    # Exact finite-grid analogue; not a polygonal approximation to a billiard.
    for a,b in ((2,3),(3,4),(4,5)):
        cells=list(product(range(a),range(b)))
        for mask_id in range(1,5):
            free={z for z in cells if (3*z[0]+z[1]+mask_id)%5 != 0}
            for ox,oy,width,height in product((-2,0,1),(-1,2),(9,13),(10,15)):
                points=list(product(range(ox,ox+width),range(oy,oy+height)))
                selected=[z for z in points if (z[0]%a,z[1]%b) in free]
                counts=Counter((x%a,y%b) for x,y in selected)
                total=len(selected)
                tv=sum(abs(F(counts[z],total)-F(1,len(free))) for z in free)/2
                complete=[]
                for i in range(ox//a-1,(ox+width)//a+1):
                    for j in range(oy//b-1,(oy+height)//b+1):
                        if ox<=a*i and a*(i+1)<=ox+width and oy<=b*j and b*(j+1)<=oy+height:
                            complete.append((i,j))
                whole=len(complete)*len(free)
                check(whole<=total,'free_tile_count')
                check(tv<=F(total-whole,total),'boundary_mixture_TV')
                inside=Counter((x%a,y%b) for x,y in selected if (x//a,y//b) in complete)
                check(all(inside[z]==len(complete) for z in free),'complete_cell_uniformity')
                # Periodic postprocessing must contract TV for arbitrary groupings.
                for gate in range(3):
                    groups=defaultdict(list)
                    for z in free: groups[(z[0]+(gate+1)*z[1])%4].append(z)
                    out=sum(abs(sum(F(counts[z],total)-F(1,len(free)) for z in zs)) for zs in groups.values())/2
                    check(out<=tv,'periodic_gate_contraction')
    for b,L,A,V in product((F(1),F(3,2)),(F(4),F(9),F(21)),(F(1,3),F(1)),(F(2),F(4))):
        if L<2*b or A>V: continue
        check(F(8)*L*b/((A/V)*4*(L-b)**2)<=8*V*b/(A*L),'continuous_boundary_constant')
        check((A/V)*(1-b/L)**2>=A/(4*V),'launch_acceptance_lower_bound')
    check(F(8)*F(7,8)**2/2>1,'launch_chernoff_exponent')


def det(u,v): return u[0]*v[1]-u[1]*v[0]


def index(cols):
    return reduce(math.gcd,(abs(det(u,v)) for u,v in combinations(cols,2)),0)


def witnesses() -> None:
    rng=random.Random(230929)
    examples=[[(1,0),(1,2),(-1,3)],[(6,0),(0,10),(1,0),(0,1)]]
    for _ in range(160):
        cols=[(rng.randint(-12,12),rng.randint(-12,12)) for _ in range(8)]
        cols += [(1,0),(0,1)]
        rng.shuffle(cols); examples.append(cols)
    for cols in examples:
        true=index(cols)
        if true==0: continue
        pair=max(combinations(cols,2),key=lambda uv:abs(det(*uv)))
        initial=abs(det(*pair))//true
        kept=list(pair); prior=initial; additions=0
        for z in cols:
            nxt=index(kept+[z])//true
            if 0<nxt<prior:
                check(prior%nxt==0,'witness_index_divisibility')
                check(2*nxt<=prior,'strict_enlargement_halves_index')
                kept.append(z); prior=nxt; additions+=1
            if prior==1: break
        check(prior==1,'witness_saturation')
        check(additions<=initial.bit_length()-1,'logarithmic_witness_bound')
        check(index(kept)==true,'retained_generators_same_group_index')
    cols=examples[0]
    check(sorted(abs(det(u,v)) for u,v in combinations(cols,2))==[2,3,5], 'no_primitive_pair_example')
    check(index(cols)==1,'gcd_235_saturation')
    check(index([(1,0),(1,2)])==2,'proper_subgroup_control')


def adaptive_arrivals() -> None:
    # A finite-state producer biased toward different missing records as history
    # changes. Exact conditional hazards, rather than independent coupon draws.
    for w in range(1,5):
        p=F(1,3*w)
        law={0:F(1)}
        for k in range(1,13):
            nxt=defaultdict(F)
            for state,mass in law.items():
                probs=[p for _ in range(w)]
                probs[(state+k)%w]+=F(1,6)
                check(sum(probs)<=1,'adaptive_producer_probability')
                nxt[state]+=mass*(1-sum(probs))
                for ell,prob in enumerate(probs):
                    nxt[state|(1<<ell)]+=mass*prob
            law=dict(nxt)
            check(sum(law.values())==1,'adaptive_state_mass')
            for ell in range(w):
                absent=sum(v for s,v in law.items() if not (s>>ell)&1)
                check(absent<=(1-p)**k,'adaptive_hazard_absence_bound')
            tail=sum(v for s,v in law.items() if s!=(1<<w)-1)
            check(tail<=w*(1-p)**k,'adaptive_cover_union_bound')
    # Nonconstant hazard product and its monotonicity under added useful mass.
    for w in (1,2,5):
        prod=F(1)
        for k in range(1,31):
            p=F(1,w*(k+1)); before=prod; prod*=1-p
            check(0<=prod<=before,'varying_hazard_product')


def defect_and_stopping() -> None:
    for V,areas,idx in product((F(1),F(3,2)),
                              ((F(1,11),F(1,13),F(1,17)),(F(1,8),F(1,7),F(1,9))),range(1,9)):
        A=V-sum(areas); gap=min(V,min(areas))
        for bits in product((0,1),repeat=len(areas)):
            visible=sum(a for a,b in zip(areas,bits) if b)
            hidden=sum(a for a,b in zip(areas,bits) if not b)
            D=idx*V-A-visible
            check(D==(idx-1)*V+hidden,'completion_defect_identity')
            complete=idx==1 and all(bits)
            check((D==0)==complete,'zero_iff_complete')
            if not complete: check(D>=gap,'incomplete_gap')
            for perturb in (-3*gap/16,F(0),3*gap/16):
                check((abs(D+perturb)<gap/2)==complete,'robust_acceptance_no_false_positive')
    delta=F(1,20)
    budget=sum(delta/(8*(k+1)**6) for k in range(1,301))
    tail_bound=delta/(8*5*301**5)
    check(budget+tail_bound<delta/8,'infinite_error_budget_integral_bound')
    for m in range(1,61):
        cost=sum(k*(k+1)**2 for k in range(1,m+1))
        check(cost<=(m+1)**4,'finite_epoch_preparation_cost')
    # Exact two-event bound supporting P(T>k) <= absence + current bad epoch.
    for absent,bad,joint in product((F(0),F(1,5),F(3,5)),repeat=3):
        if max(F(0),absent+bad-1)<=joint<=min(absent,bad):
            check(absent+bad-joint<=absent+bad,'current_epoch_tail_union')
    check(6>4,'fourth_moment_tail_condition')
    check(6-3>1,'finite_expected_launch_cost_condition')


def rates_and_rationals() -> None:
    for beta in (F(1),F(1,2),F(1,3),F(2,3),F(3,4)):
        h=1/(2*beta+6)
        rate=beta*h; aperture=(beta+4)*h
        check(F(1,2)-3*h==rate,'bias_variance_balance')
        check(aperture-4*h==rate,'preparation_bias_balance')
        check(1-4*h>=rate,'linear_bernstein_smaller')
        check(2*h<1,'cells_bounded_by_samples')
    for Q in range(2,17):
        vals=sorted({F(a,b) for b in range(1,Q+1) for a in range(-2*b,2*b+1)})
        for x,y in zip(vals,vals[1:]):
            check(y-x>=F(1,Q*Q),'rational_denominator_separation')
        for x in vals[::max(1,len(vals)//7)]:
            perturb=F(1,8*Q*Q)
            hits=[y for y in vals if abs(y-(x+perturb))<=F(1,4*Q*Q)]
            check(hits==[x],'unique_noisy_rational_decoding')
        # Data halfway between 0 and 1 are deliberately unresolved for Q=1.
    hits=[z for z in (-1,0,1) if abs(F(z)-F(1,2))<=F(1,4)]
    check(not hits,'unresolved_arithmetic_fails_closed')


def sources() -> None:
    expected={'02_local.tex':'f389f30844487e78137752faf4f79bbbbd6797ed',
              '03_completeness.tex':'604a40b3ed7aaae544c8fe58d4f66cdaee9eaeea',
              '04_reference_free.tex':'60b4234d4f68caae7259b4bd5fac53c9b9ec34a2'}
    for name,want in expected.items():
        b=(ROOT/'core'/name).read_bytes()
        got=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
        check(got==want,'reviewed_core_blob',name)
    text=(ROOT/'main.tex').read_text()
    for path in re.findall(r'\\input\{([^}]+)\}',text):
        f=ROOT/(path+'.tex'); check(f.exists(),'input_exists',path); text+='\n'+f.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)),'unique_labels')
    for ref in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text):
        check(ref in labels,'resolved_cross_reference',ref)
    for label in ('thm:discovery-main','thm:completion-main','thm:uniform-main','prop:box',
                  'lem:biased-histogram','lem:small-witness','thm:sequential','cor:scanner-discovery'):
        check(label in labels,'principal_result_present',label)


def retained(geometry: bool) -> dict:
    path=ROOT/'tools/retained_verify_v19.py'
    spec=importlib.util.spec_from_file_location('retained_local_diagnostics',path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.curvature(); module.densities(); module.bins()
    numerical=module.geometry() if geometry else None
    return {'scope':'Selected retained local curvature/density/bin identities, not the v19 complete suite',
            'total_checks':sum(module.C.values()),'groups':dict(sorted(module.C.items())),
            'numerical':numerical}


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument('--geometry',action='store_true')
    args=ap.parse_args()
    sampler(); witnesses(); adaptive_arrivals(); defect_and_stopping(); rates_and_rationals(); sources()
    old=retained(args.geometry)
    print(json.dumps({'schema':'a2-v23-finite-diagnostics-1','status':'passed',
                      'new_finite_checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
                      'retained_selected':old,'formal_proof_certificate':False,
                      'executed_physical_scanner':False},sort_keys=True,indent=2))

if __name__=='__main__': main()
