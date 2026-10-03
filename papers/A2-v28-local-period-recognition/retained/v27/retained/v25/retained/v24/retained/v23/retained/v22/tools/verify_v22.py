#!/usr/bin/env python3
"""Finite A2 v22 diagnostics. Explicit checks remain active under python -O."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import random
import re

from certificate import (column_hnf, completion_decision, determinant,
                         extended_gcd, recover_cycles, bounded_rational)
import verify_local_basis as retained

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()


def check(ok: bool, group: str, detail: object = '') -> None:
    if not ok:
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] += 1


def defects() -> None:
    for V, visible, missing, m in product([F(1), F(3,2), F(5,2)],
            [F(1,10), F(1,4), F(1,2)], [F(0),F(1,20),F(1,5)], range(1,8)):
        A = V-visible-missing
        d = m*V-A-visible
        check(d == (m-1)*V+missing, 'completion_identity')
        check(d >= 0 and ((d == 0) == (m == 1 and missing == 0)), 'zero_iff_complete_saturated')
        check(d == 0 or d >= min(V,F(1,20)), 'uniform_positive_gap')
    vectors=[(1,0),(1,2),(-1,3)]
    check([abs(determinant(a,b)) for a,b in combinations(vectors,2)] == [2,3,5], 'no_primitive_pair')
    check(column_hnf(vectors) == ((1,0),(0,1)), 'all_cycle_saturation')
    check(column_hnf(vectors[:2]) == ((1,0),(0,2)), 'proper_subgroup_detected')
    # A+visible is deliberately wrong as a period calibration before coverage.
    V, visible, hidden = F(1), F(1,5), F(1,7)
    check(F(2)/(V-hidden) == F(7,3), 'premature_area_calibration_not_integral')
    check(F(2)-((V-visible-hidden)+visible) == 1+hidden, 'index_and_hidden_area_add')


def hermite_checks() -> None:
    for a,b in product(range(-8,9),repeat=2):
        g,x,y=extended_gcd(a,b)
        check(g == math.gcd(a,b) and a*x+b*y==g, 'bezout_signed_and_zero')
    rng=random.Random(220929)
    count=0
    while count<350:
        vectors=[(rng.randint(-9,9),rng.randint(-9,9)) for _ in range(5)]
        g=0
        for u,v in combinations(vectors,2): g=math.gcd(g,abs(determinant(u,v)))
        if not g: continue
        H=column_hnf(vectors); a,b=H[0]; c=H[1][1]
        check(a*c==g and 0<=b<a and c>0,'hermite_determinantal_index')
        for x,y in vectors:
            check(y%c==0 and (x-b*(y//c))%a==0,'hermite_contains_every_generator')
        changed=list(reversed(vectors))+[vectors[0],(0,0),(-vectors[1][0],-vectors[1][1])]
        check(column_hnf(changed)==H,'duplicate_reversal_order_invariance')
        sheared=[(x+3*y,y) for x,y in vectors]
        H2=column_hnf(sheared)
        check(H2[0][0]*H2[1][1]==g,'unimodular_frame_index_invariance')
        count+=1


def rational_and_noisy_checks() -> None:
    for Q in range(1,13):
        vals=sorted({F(p,q) for q in range(1,Q+1) for p in range(-2*q,2*q+1)})
        for x,y in zip(vals,vals[1:]):
            check(y-x>=F(1,Q*Q),'bounded_denominator_separation')
        for x in vals[::max(1,len(vals)//9)]:
            radius=1/(4*Q*Q)
            check(bounded_rational(float(x)+radius/4,Q,radius)==x,'unique_rational_decoding')
    rng=random.Random(221)
    base=[(1,0),(1,2),(-1,3)]
    for shear,scale,hidden,use_all in product(range(-2,3),[1.,1.5],[0.,.08],[False,True]):
        true=[(scale*(x+shear*y),y) for x,y in (base if use_all else base[:2])]
        true += [true[0],(-true[0][0],-true[0][1])]
        noisy=[(x+rng.uniform(-1e-13,1e-13),y+rng.uniform(-1e-13,1e-13)) for x,y in true]
        B=math.ceil(max(math.hypot(*v) for v in true))+1
        rec=recover_cycles(noisy,vector_error=2e-13,true_norm_bound=B,covolume_lower=1.)
        expected=(1 if use_all else 2)*scale
        check(rec.rank_two and abs(rec.covolume-expected)<1e-9,'noisy_group_covolume')
        A=scale-.2-hidden
        decision=completion_decision(rec,free_area=A,visible_area_sum=.2,
                    combined_area_error=1e-10,covolume_lower=1.,body_area_lower=.05)
        check(decision['accepted']==(use_all and hidden==0),'noisy_completion_decision')
        check(abs(decision['defect']-((0 if use_all else scale)+hidden))<1e-9,'noisy_defect_decomposition')
    rank1=recover_cycles([(1.,0.),(2.,0.),(3.,0.)],vector_error=1e-12,
                          true_norm_bound=4.,covolume_lower=1.)
    check(not rank1.rank_two,'rank_deficient_not_certified')
    try:
        recover_cycles([(1.,0.),(0.,1.)],vector_error=.1,
                       true_norm_bound=2.,covolume_lower=1.)
    except ValueError:
        check(True,'insufficient_precision_fails_closed')
    else:
        check(False,'insufficient_precision_fails_closed')


def testing_and_rates() -> None:
    for A,p0,a in product([F(1),F(2),F(3)], [F(1,10),F(1,4),F(1,2)],
                         [F(1,1000),F(1,100),F(1,20)]):
        p=p0*A/(A-a)
        check(A*(1-p0/p)==a,'hidden_area_mass_inversion')
        check((p-p0)==p0*a/(A-a),'linear_area_signal')
        pp,qq=float(p0),float(p)
        kl=pp*math.log(pp/qq)+(1-pp)*math.log((1-pp)/(1-qq))
        chi=(pp-qq)**2/(qq*(1-qq))
        check(-1e-15<=kl<=chi+1e-15,'bernoulli_entropy_upper_bound')
    for beta in [F(1),F(1,2),F(1,3),F(2,3),F(3,4)]:
        t=1/(2*beta+6)
        check(beta*t==F(1,2)-3*t,'bias_variance_balance')
        check(1-4*t>beta*t,'linear_bernstein_term_smaller')
    for s,p,m in product([1,2,5,11],[F(1,4),F(1,2),F(3,4)],range(1,12)):
        exact_all=(1-(1-p)**m)**s
        check(1-exact_all<=s*(1-p)**m,'random_retention_union_bound')
    # Truncated error spending is below delta, not falsely equal to it.
    spent=sum(6/(math.pi**2*m*m) for m in range(1,10001))
    check(spent<1 and spent>.9999,'sequential_error_spending')


def sources() -> None:
    local=(ROOT/'core/02_local.tex').read_bytes()
    gitsha=hashlib.sha1(f'blob {len(local)}\0'.encode()+local).hexdigest()
    check(gitsha=='f389f30844487e78137752faf4f79bbbbd6797ed','unchanged_intrinsic_local_proof')
    text=(ROOT/'main.tex').read_text()
    for item in re.findall(r'\\input\{([^}]+)\}',text):
        path=ROOT/(item+'.tex')
        check(path.is_file(),'reachable_primary_input')
        text+='\n'+path.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)),'unique_primary_labels')
    for label in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
        check(label in labels,'resolved_primary_reference',label)
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    for block in re.findall(r'\\cite(?:\[[^\]]*\])*\{([^}]+)\}',text):
        for key in block.split(','): check(key in bib,'resolved_bibliography',key)
    for key in ('thm:completion-main','lem:rational','cor:defect-gap','thm:area-testing'):
        check(key in labels,'new_mathematical_component',key)


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument('--geometry',action='store_true')
    args=ap.parse_args()
    defects(); hermite_checks(); rational_and_noisy_checks(); testing_and_rates(); sources()
    # Run only the actually reused local algebra/geometry functions. Do not
    # relabel the historical script's complete v19 suite or source checks.
    retained.C.clear()
    retained.curvature(); retained.densities(); retained.bins()
    numerical=retained.geometry() if args.geometry else None
    print(json.dumps({'schema':'a2-v22-finite-diagnostics-1','status':'passed',
          'new_checks':sum(COUNTS.values()),'new_groups':dict(sorted(COUNTS.items())),
          'retained_local_subset_checks':sum(retained.C.values()),
          'retained_local_subset_groups':dict(sorted(retained.C.items())),
          'numerical':numerical,'formal_proof_certificate':False,
          'scope':'Finite arithmetic, error-control diagnostics, local curvature tests and source consistency only'},
          indent=2,sort_keys=True))

if __name__=='__main__': main()
