#!/usr/bin/env python3
"""Exact finite diagnostics for scalar recovery and atomic collar currents.

These fixtures test algebra, signs, weights and negative controls. They do
not certify Lorentz realizability or an ordered continuum height estimate.
"""
from fractions import Fraction as Q
import json
import random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def recovery(x, overlap, receiving, controlled, loss, distortion=Q(1), reserve=Q(1)):
    values = (x, overlap, receiving, controlled, loss)
    if min(values) < 0 or distortion <= 0 or reserve < 1:
        raise ValueError('nonnegative capacities, positive distortion, reserve >= 1 required')
    if overlap > min(x, receiving) or controlled > distortion*overlap or loss > distortion*(x-overlap):
        raise ValueError('physical capacity bounds violated')
    theta = min(Q(1), (reserve*receiving-overlap)/(x-overlap)) if x > overlap else Q(1)
    return theta, controlled+theta*loss, (1-theta)*loss


def value(edges, values, u):
    for a, b, v in zip(edges, edges[1:], values):
        if a < u < b:
            return v
    raise ValueError('evaluation must be inside a cell, not on a jump')


def average(edges, values, j):
    return sum((max(Q(0), min(b,j)-a)*v for a,b,v in zip(edges,edges[1:],values)), Q(0))/j


def fdist(j, s):
    return min(s/j, Q(1))


def kernel(j, u, s):
    if u == s:
        raise ValueError('choose a continuity point')
    return fdist(j,s) if s < u else -(1-fdist(j,s))


def atomic_balance(edges, values, j, u):
    return sum((kernel(j,u,s)*(right-left)
                for s,left,right in zip(edges[1:-1],values,values[1:])), Q(0))


def finite_checks():
    rng = random.Random(710155156)
    counts = {'capacity_cases':0, 'atomic_profile_evaluations':0, 'weighted_translated_cases':0}
    for _ in range(1200):
        x,y = Q(rng.randrange(25),7), Q(rng.randrange(25),7)
        o = min(x,y)*Q(rng.randrange(8),7)
        e = Q(rng.randrange(1,9),3)
        s = e*o*Q(rng.randrange(8),7)
        d = e*(x-o)*Q(rng.randrange(8),7)
        previous = d
        for k in (Q(1),Q(3,2),Q(2),Q(5)):
            theta,sk,dk = recovery(x,o,y,s,d,e,k)
            require(0 <= theta <= 1 and sk+dk == s+d, 'positive exact source split')
            require(sk >= s and 0 <= dk <= min(d,previous), 'monotone recovery')
            require(sk <= e*min(x,k*y), 'controlled receiving height')
            require(dk <= e*max(Q(0),x-k*y), 'residual capacity height')
            require(o+theta*(x-o) == min(x,k*y), 'maximal unused-capacity allocation')
            previous = dk
            counts['capacity_cases'] += 1
    edges = [Q(i,8) for i in range(9)]
    j = Q(1,2)
    for _ in range(180):
        vals = [Q(rng.randrange(7),6) for _ in range(8)]
        avg = average(edges,vals,j)
        for a,b in zip(edges,edges[1:]):
            u=(a+b)/2
            cur=atomic_balance(edges,vals,j,u)
            require(cur == value(edges,vals,u)-avg, 'signed BV identity including jump atoms')
            bound=Q(0)
            for s,left,right in zip(edges[1:-1],vals,vals[1:]):
                jump=right-left
                if s < u:
                    bound += fdist(j,s)*max(jump,Q(0))
                elif s > u:
                    bound += (1-fdist(j,s))*max(-jump,Q(0))
            require(max(cur,Q(0)) <= bound, 'two-sided directed Jordan bound')
            counts['atomic_profile_evaluations'] += 1
    # Unequal physical weights, different critical values and nonconstant guards.
    for _ in range(160):
        profiles=[[Q(rng.randrange(6),5) for _ in range(8)] for _ in range(3)]
        weights=[Q(rng.randrange(1,9),4) for _ in range(3)]
        centers=[Q(-1,16),Q(0),Q(1,16)]
        t=Q(13,32)
        x=y=o=cur=old_s=old_d=Q(0)
        for z,(vals,w,tz) in enumerate(zip(profiles,weights,centers)):
            u=t-tz
            v=value(edges,vals,u)
            av=average(edges,vals,j)
            ov=average(edges,[min(v,q) for q in vals],j)
            x+=w*v; y+=w*av; o+=w*ov
            cur+=w*atomic_balance(edges,vals,j,u)
            guard=Q(z+1,4)
            old_s+=w*ov*guard
            old_d+=w*(v-ov)*guard
        require(cur == x-y, 'weights and common-roof translations before summing')
        _,s,d=recovery(x,o,y,old_s,old_d)
        require(s <= y and d <= max(cur,Q(0)), 'guarded pooled source bound')
        counts['weighted_translated_cases'] += 1
    rejected=[]
    def reject(name, wrong_claim):
        require(not wrong_claim, 'negative control failed to reject: '+name)
        rejected.append(name)
    # Isolated late birth is invisible to a negative-current-only estimate.
    e=[Q(0),Q(3,4),Q(1)]; v=[Q(0),Q(1)]; u=Q(7,8)
    birth=atomic_balance(e,v,j,u)
    reject('negative current alone controls inward whole-disk comparison', birth <= 0)
    reject('classical derivative retains an atomic birth', birth == 0)
    theta,_,residual=recovery(Q(1),Q(0),Q(0),Q(0),Q(1),reserve=Q(100))
    reject('finite receiving reserve recovers an isolated unsupported birth', residual == 0)
    # Complementary equal-center profiles: positive parts must follow summation.
    c1,c2=Q(1),Q(-1)
    reject('positive part can precede chart summation', max(c1,0)+max(c2,0) == max(c1+c2,0))
    _,sc,dc=recovery(Q(1),Q(0),Q(1),Q(0),Q(1))
    require(sc == 1 and dc == 0, 'complementary capacity recovery')
    reject('physical Jacobian weights can be discarded', 2*c1+c2 == c1+c2)
    vals=[Q(0)]*4+[Q(1)]*4
    reject('different critical values can share a radial evaluation',
           value(edges,vals,Q(9,16)) == value(edges,vals,Q(7,16)))
    # Never pool distinct exact labels: one has loss, the other has reserve.
    own=recovery(Q(1),Q(0),Q(0),Q(0),Q(1))[2]
    wrongly_crossed=recovery(Q(1),Q(0),Q(1),Q(0),Q(1))[2]
    reject('capacity may be borrowed across exact labels', own == wrongly_crossed)
    x,o,y=Q(2),Q(1),Q(1)
    wrong_theta=min(Q(1),y/(x-o))
    reject('already used overlap need not be deducted', o+wrong_theta*(x-o) <= y)
    _,s,d=recovery(Q(2),Q(0),Q(1),Q(0),Q(2))
    reject('controlled and residual weights are disjoint events', s*d == 0)
    try:
        recovery(Q(1),Q(0),Q(1),Q(0),Q(1),reserve=Q(1,2))
    except ValueError:
        rejected.append('reserve below one')
    else:
        raise RuntimeError('invalid reserve accepted')
    require(Q(6)*Q(1,2)*Q(1,12) == Q(1,4), 'legal chi^6 band exponent')
    require(Q(1,8)-Q(1,4) < 0, 'fixed-band growing reserve example')
    return {'counts':counts, 'negative_controls_rejected':rejected,
            'exact_fraction_arithmetic':True, 'unchanged_source_weights':True,
            'birth_and_death_atoms_retained':True, 'common_roof_weighted_cancellation':True,
            'fixtures_claimed_as_Lorentz_realizations':False,
            'collision_uniform_net_current_bound_certified':False,
            'continuum_proof_certified':False}


if __name__ == '__main__':
    print(json.dumps(finite_checks(), indent=2, sort_keys=True))
