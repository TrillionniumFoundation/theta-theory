#!/usr/bin/env python3
"""Exact rational regression fixtures; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def checks() -> dict:
    counts: dict[str, int] = {}
    def check(group: str, condition: bool) -> None:
        require(condition, group)
        counts[group] = counts.get(group, 0) + 1

    pmax = 2*F(53,100)/(1+F(53,100)**2)+F(1,200)
    check('collar', pmax < F(17,20))
    rminus, upper = F(9,20), F(47,6)
    rcol = rminus**2/(800*upper)
    check('collar', 2*upper*rcol/rminus**2 == F(1,20)**2)
    check('collar', F(17,20)+F(1,20) < F(19,20))
    vals = (F(0), F(1,4), F(1,2), F(1))
    for a0, a1, w0, w1 in itertools.product((F(1,10),F(1),F(4)),
                                            (F(1,100),F(1,2),F(2)), vals, vals):
        k = abs(w0-w1)
        check('capped_guard', min(a0,a1)*w0 <= a1*(w1+k))
    densities = (F(1,100), F(1,2), F(1), F(3))
    for ds, labels in itertools.product(itertools.product(densities,repeat=3),
                                        itertools.product((0,1),repeat=3)):
        a0 = F(1); dt = F(1,3)
        clock = sum((dt*l*min(F(1),a/a0) for a,l in zip(ds,labels)),F(0))
        anchor = sum((dt*l*a for a,l in zip(ds,labels)),F(0))
        for q in (F(1,8),F(1,4),F(1,2)):
            if clock >= q:
                check('capped_anchor', a0 <= anchor/q)
        for D,beta in itertools.product((F(1),F(2),F(4)),(F(1,4),F(1,2),F(1))):
            if min(ds) >= 1/D and sum(labels)*dt >= beta:
                check('old_admission_containment', clock >= beta/D)
    # Abstract occupations demonstrate distinct tests, not realized billiard trajectories.
    check('abstract_recovery', F(3,5)+F(3,5) >= F(1,8))
    check('abstract_recovery', F(15,16)+F(1,16)*F(1,100) >= F(1,8))
    check('abstract_recovery', 1/F(1,100) > 2)
    check('abstract_recovery', F(1,5) < F(1,4) and 2*F(1,5) >= F(1,8))
    for path in itertools.product(densities,repeat=4):
        a0 = path[0]
        variation = sum((abs(path[i+1]-path[i]) for i in range(3)),F(0))
        for D in (F(3,2),F(2),F(5)):
            if min(path) < a0/D:
                check('running_loss', a0 <= variation/(1-1/D))
    for q in (F(1,16),F(1,8),F(1,4),F(1,2)):
        d=2*q
        for ratios in itertools.product(densities,repeat=3):
            partial_clock=d*sum((min(F(1),v) for v in ratios),F(0))/3
            if partial_clock < q:
                check('low_clock_running_loss', min(ratios)<F(1,2))
        for tm,tp,z,a in itertools.product((F(0),q,2*q,4*q,8*q),
                                           (q,2*q,4*q,8*q),
                                           (F(0),F(1,8),F(1)),
                                           (F(1,8),F(1,2))):
            pm=tm>4*q
            pp=not pm and z>=a and tp>2*q
            remainder=not (pm or pp)
            check('disjoint_partition', int(pm)+int(pp)+int(remainder)==1)
            check('exact_complement', remainder == (tm<=4*q and (z<a or tp<=2*q)))
            if remainder:
                check('residual_support', (tm<=4*q and z<a) or tm+tp<=6*q)
        lam=F(1,5)
        for tm,s in itertools.product((5*q,8*q,10*q),(F(0),q,2*q)):
            check('backward_radial_cutoff', 2*lam*(tm-s)>4*lam*q)
    check('outer_schedule', F(1,12)*F(1,16)==F(1,192))
    check('mass_exponents', F(129,128)/2==F(129,256))
    check('mass_exponents', F(1,32)<F(129,256))
    for tau in (F(0),F(1,64),F(1,32)):
        N=2*(1+tau)+1
        check('outer_schedule', F(1,16)-tau>0 and N/2-1-tau>0 and N+tau>0)
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational algebra, abstract occupation and path fixtures only',
            'independent_human_review':False,'formal_proof_certificate':False,
            'full_pointwise_LLT_proved':False}

if __name__=='__main__':
    print(json.dumps(checks(),sort_keys=True,indent=2))
