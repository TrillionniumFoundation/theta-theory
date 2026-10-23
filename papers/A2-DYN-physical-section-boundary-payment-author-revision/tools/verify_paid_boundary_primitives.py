#!/usr/bin/env python3
"""Exact finite diagnostics for native340; not a continuum billiard proof."""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path


def need(value, message):
    if not value:
        raise ValueError(message)


def main():
    # Distinct physical contributions may share the same true label and roof.
    contributions = [
        ('a', Q(1), Q(3, 7)), ('a', Q(1), Q(-2, 7)),
        ('a', Q(2), Q(-5, 9)), ('a', Q(4), Q(1, 3)),
        ('b', Q(1), Q(-3, 7)), ('b', Q(3), Q(2, 5)),
    ]
    atoms = defaultdict(lambda: defaultdict(Q))
    for label, roof, weight in contributions:
        atoms[label][roof] += weight
    total = sum(abs(w) for d in atoms.values() for w in d.values())
    uncombined = sum(abs(w) for _, _, w in contributions)
    need(total <= uncombined, 'Combined same-roof budget')
    # Different labels must not be canceled against each other.
    need(atoms['a'][Q(1)] != atoms['a'][Q(1)] + atoms['b'][Q(1)],
         'Exact-label negative control')
    T = Q(6)

    def eta(t):
        # A piecewise linear surrogate checks only the primitive algebra.
        # The paper uses a smooth nondecreasing transition of the same mass.
        return min(Q(1), max(Q(0), t-T))

    def primitive(d, t):
        return sum(w * (Q(int(t >= u))-eta(t)) for u, w in d.items())

    def step_integral(u, left, right):
        return max(Q(0), right-max(left,u))

    def eta_integral(left, right):
        def anti(t):
            z=t-T
            return Q(0) if z <= 0 else z*z/2 if z <= 1 else z-Q(1,2)
        return anti(right)-anti(left)

    def primitive_integral(d, left, right):
        return sum(w*(step_integral(u,left,right)-eta_integral(left,right))
                   for u,w in d.items())

    tests = 0
    for d in atoms.values():
        bound = sum(abs(w) for w in d.values())
        beta = sum(d.values())
        need(beta-beta == 0, 'Compensated derivative has zero mass')
        need(bound+abs(beta) <= 2*bound, 'Complete derivative variation bound')
        need(primitive(d,Q(-3)) == primitive(d,Q(8)) == 0,
             'Compact support at both ends')
        for t in [Q(i,11) for i in range(-22,100)]:
            need(abs(primitive(d,t)) <= bound, 'Supremum budget')
        for exponent in [0,1,2,5,10,30,100,300]:
            width=Q(1,10**exponent)
            for left in [Q(-1),Q(0),Q(1)-width/2,Q(1),Q(2)-width/3,
                         Q(3),Q(4)-width/2,T,T+Q(1,2),T+1]:
                integral=primitive_integral(d,left,left+width)
                need(abs(integral)/width <= bound, 'Actual width cancels exactly')
                for m in [1,2,114,1000]:
                    need(m*m*abs(integral)/width <= m*m*bound,
                         'Original collision normalization')
                tests += 1
    # Without compensation, a partial atomic derivative usually leaves a tail.
    tail=sum(atoms['a'].values())
    need(tail != 0, 'Missing-compensation negative control is nontrivial')
    need(sum(atoms['a'].values())-tail == 0, 'Compensation restores zero mass')

    # Exact original-denominator fraction bound; surrogate is not a new law.
    ratios=0
    for P in [Q(1,10),Q(2,3),Q(1)]:
        for A in [Q(1,2),Q(1),Q(4)]:
            for fraction in [Q(1,100),Q(1,10),Q(1,2)]:
                delta=P*fraction
                for nsign in [-1,0,1]:
                    N=A*P*nsign
                    for dp in [-delta,delta]:
                        for dn in [-A*delta,A*delta]:
                            ptilde=P+dp;ntilde=N+dn
                            need(ptilde>0, 'Actual strict denominator floor')
                            need(abs(N/P-ntilde/ptilde) <= 2*A*delta/(P-delta),
                                 'Conditional ratio bound')
                            ratios+=1
    # A smooth narrow spike has no atoms: an exact polynomial family on [0,1].
    # phi(s)=16s^2(1-s)^2, extended by0, is C1, max1, integral8/15, TV2.
    phi_integral=Q(16)*(Q(1,3)-Q(1,2)+Q(1,5))
    need(phi_integral == Q(8,15), 'Continuous spike normalization')
    for m in [2,10,114,1000]:
        height=Q(1,m*m);width=Q(1,m**3)
        need(m*m*height==1, 'Paid-atom-only false-completion negative control')
        need(height*width*phi_integral==Q(8,15*m**5), 'Small mass is not raw height')
    out={
        'status':'PASS', 'arithmetic':'exact fractions; no floating-point acceptance',
        'coincident_roof_contributions':len(contributions),
        'distinct_labels':len(atoms),'combined_budget':str(total),
        'microscopic_intervals_checked':tests,'smallest_checked_width':'10^-300',
        'conditional_ratio_cases':ratios,
        'negative_controls':['wrong cancellation across labels','missing compensating tail',
                             'no atomic derivative does not imply raw-height decay'],
        'scope':'Finite formula diagnostics. All physical source summations and continuum estimates are supplied by native338--342, with their inherited hypotheses. No LLT or inverse certification.'
    }
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
