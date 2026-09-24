#!/usr/bin/env python3
"""Exact finite diagnostics for the compatible-frontier revision.

These checks supplement, and do not certify, the analytic proofs. No floating
point optimization, solver output, or assertion statement is used as evidence.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from itertools import combinations, product
import json
from typing import Iterable

CHECKS = 0
MUTANT = None


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def midpoint_value(p: Q) -> Q:
    factor = Q(1, 2) if MUTANT == 'minimax-as-bayes' else Q(1, 3)
    return 1-p+factor*p*(1-p)*(1-2*p)


def psi(r: tuple[Q, Q]) -> Q:
    denominator = (2 if MUTANT == 'wrong-terminal-denominator' else 1)
    return Q(1, 2)+abs(r[1]-r[0])/(2*(denominator+abs(1-r[0]-r[1])))


def canonical(z: Iterable[tuple[Q, Q]]) -> tuple[tuple[Q, Q], ...]:
    return tuple(sorted((x for x in z if sum(x)), key=lambda x: (x[1]/sum(x), x)))


def merge_atoms(atoms: tuple[tuple[Q, Q], ...], k: int, intervals: bool):
    if not atoms:
        raise ValueError('empty experiment')
    atoms = canonical(atoms)
    seen = set()
    if intervals:
        for blocks in range(1, min(k, len(atoms))+1):
            for cuts in combinations(range(1, len(atoms)), blocks-1):
                bounds = (0,)+cuts+(len(atoms),)
                out = canonical(tuple((sum((a[0] for a in atoms[lo:hi]), Q(0)),
                                       sum((a[1] for a in atoms[lo:hi]), Q(0)))
                                      for lo, hi in zip(bounds, bounds[1:])))
                if out not in seen:
                    seen.add(out)
                    yield out
    else:
        for f in product(range(k), repeat=len(atoms)):
            sums = [[Q(0), Q(0)] for _ in range(k)]
            for a, j in zip(atoms, f):
                sums[j][0] += a[0]
                sums[j][1] += a[1]
            out = canonical(tuple(map(tuple, sums)))
            if out not in seen:
                seen.add(out)
                yield out


def bayes_reachable(prior, experiments, profile, payoff, intervals):
    # An experiment is a list of available actions. Each action holds the two
    # conditional report rows. Action indices are selected per retained state.
    current = {((prior[0], prior[1]),)}
    peak_lists = 1
    for actions, k in zip(experiments, profile):
        following = set()
        for z in current:
            for chosen in product(range(len(actions)), repeat=len(z)):
                atoms = []
                for masses, action in zip(z, chosen):
                    for p0, p1 in zip(*actions[action]):
                        a = (masses[0]*p0, masses[1]*p1)
                        if sum(a):
                            atoms.append(a)
                following.update(merge_atoms(tuple(atoms), k, intervals))
        current = following
        peak_lists = max(peak_lists, len(current))
    def score(z):
        return sum((max(a*payoff[0][j]+b*payoff[1][j]
                        for j in range(len(payoff[0]))) for a,b in z), Q(0))
    return max(map(score, current)), peak_lists


def conditional_atoms(p: Q, r: tuple[Q, Q]):
    return tuple(((r[0] if m else 1-r[0])*(p if y else 1-p),
                  (r[1] if m else 1-r[1])*(1-p if y else p))
                 for m,y in product(range(2), repeat=2))


def ordered_atoms(atoms):
    atoms = [a for a in atoms if sum(a)]
    return sorted(atoms, key=lambda a: (a[0] == 0,
                  a[1]/a[0] if a[0] else Q(0)),
                  reverse=MUTANT != 'wrong-roc-order')


def terminal_minimax(atoms) -> Q:
    a0 = a1 = Q(0)
    best = Q(0)
    for b0,b1 in ordered_atoms(atoms):
        best = max(best, min(1-a0, a1))
        alpha = (1-a0-a1)/(b0+b1)
        if 0 <= alpha <= 1:
            best = max(best, min(1-a0-alpha*b0, a1+alpha*b1))
        a0 += b0
        a1 += b1
    return max(best, min(1-a0, a1))


def receiver_grid(p: Q, n: int) -> Q:
    states = {(Q(0), Q(0))}
    fractions = (Q(0), Q(1,3), Q(1,2), Q(2,3), Q(1))
    for _ in range(n):
        following = set()
        for r in states:
            a0 = a1 = Q(0)
            for b0,b1 in ordered_atoms(conditional_atoms(p,r)):
                for lam in fractions:
                    following.add((a0+lam*b0, a1+lam*b1))
                a0 += b0
                a1 += b1
        states = following
    return max(map(psi, states))


def compatible(rows, shared: bool = False) -> bool:
    # rows[occurrence] contains (incoming_mass, outgoing_probability_mass_vector).
    for occurrence in rows:
        for x, flow in occurrence:
            if x < 0 or any(f < 0 for f in flow) or sum(flow) != x:
                return False
    if MUTANT == 'drop-minors':
        return True
    groups = [sum(rows, [])] if shared and MUTANT != 'shared-row-free' else rows
    for group in groups:
        for x, flow in group:
            for y, other in group:
                if any(f*y != g*x for f,g in zip(flow, other)):
                    return False
    return True


def run():
    counts = {'bayesian_peak_lists_accumulated': 0, 'rational_middle_channels': 0}
    examples = []
    payoff = ((Q(1),Q(0)),(Q(0),Q(1)))
    for p in (Q(1,8),Q(1,4),Q(3,8)):
        action = ((1-p,p),(p,1-p))
        experiment = [[action]]*3
        for k in (1,2,3):
            raw, count = bayes_reachable((Q(1,2),Q(1,2)), experiment,
                                         (2,k,2), payoff, False)
            ordered, _ = bayes_reachable((Q(1,2),Q(1,2)), experiment,
                                         (2,k,2), payoff, True)
            d = p*(1-p)*(1-2*p)
            expected = 1-p+(Q(0) if k==1 else Q(1,2) if k==2 else Q(1))*d
            require(raw == expected, 'exhaustive Bayesian profile value')
            require(ordered == raw, 'interval recursion versus unrestricted maps')
            counts['bayesian_peak_lists_accumulated'] += count
        r = (p*p,(1-p)**2)
        atoms = conditional_atoms(p,r)
        test = (Q(0),Q(2,3),Q(1),Q(1))
        false_positive = sum((a*q for (a,b),q in zip(atoms,test)), Q(0))
        power = sum((b*q for (a,b),q in zip(atoms,test)), Q(0))
        require(1-false_positive == power == midpoint_value(p), 'equal-error witness')
        require(terminal_minimax(atoms) == midpoint_value(p), 'exact terminal receiver LP')
        c0,c1 = 1-p-p*p+p**3,1-2*p*p+p**3
        mixed = (c0+c1)/2
        require(mixed-midpoint_value(p) == d/6, 'strict hidden-selector gap')
        for u,w,v in product((Q(i,4) for i in range(5)), repeat=3):
            r0=(1-p)**2*u+2*p*(1-p)*w+p*p*v
            r1=p*p*u+2*p*(1-p)*w+(1-p)**2*v
            upper = terminal_minimax(conditional_atoms(p,(r0,r1)))
            require(upper <= midpoint_value(p), 'stochastic-grid universal bound diagnostic')
            if v < u:
                u,w,v = 1-u,1-w,1-v
                r0,r1 = 1-r0,1-r1
            alpha=v-u; c=2*p*(1-p)
            if alpha:
                a=max(Q(0),u+c*(w-v))
                edge=(u+c*(w-u)-a)/(c*alpha)
            else:
                a=r0; edge=Q(0)
            s0,s1=p*p+c*edge,(1-p)**2+c*edge
            require(0 <= a <= 1-alpha and 0 <= edge <= 1, 'legal channel domination')
            require((r0,r1)==(a+alpha*s0,a+alpha*s1), 'domination reconstruction')
            counts['rational_middle_channels'] += 1
        for w in (Q(i,16) for i in range(9)):
            r0,r1=p*p+2*p*(1-p)*w,(1-p)**2+2*p*(1-p)*w
            alpha=2*(1-2*w)/(3-2*w)
            val=1-r0-alpha*(1-r0)*p
            gap=2*p*(1-p)*(1-2*p)*w*(5-6*w)/(3*(3-2*w))
            require(midpoint_value(p)-val == gap >= 0, 'factorized upper certificate')
        examples.append({'p':str(p),'Bayes_222':str(mixed),
                         'minimax_222':str(midpoint_value(p)),
                         'Bayes_and_minimax_232':str(1-p+d)})
    require(receiver_grid(Q(1,4),3)==Q(25,32), 'receiver recursion attains exact noisy value')
    for r in [(Q(0),Q(0)),(Q(1),Q(1)),(Q(0),Q(1)),(Q(1,4),Q(3,4))]:
        atoms=((1-r[0],1-r[1]),r)
        require(psi(r)==terminal_minimax(atoms),'closed terminal minimax formula')
    # Unequal priors, general payoffs, unequal and controlled noisy reports.
    actions=[((Q(3,4),Q(1,4)),(Q(1,4),Q(3,4))),
             ((Q(1,2),Q(1,2)),(Q(1,8),Q(7,8)))]
    nonbinary_payoff=((Q(1),Q(0),Q(2,3)),(Q(0),Q(1),Q(1,4)))
    for prior in [(Q(1,2),Q(1,2)),(Q(1,3),Q(2,3))]:
        for profile in [(2,2),(1,2),(2,1)]:
            a,_=bayes_reachable(prior,[actions,actions],profile,nonbinary_payoff,True)
            b,_=bayes_reachable(prior,[actions,actions],profile,nonbinary_payoff,False)
            require(a==b,'controlled/general-loss interval recursion')
    # Local and across-time compatibility, including zero-mass rows.
    u=(Q(1,3),Q(2,3))
    good=[[(x,tuple(x*a for a in u)) for x in [Q(0),Q(1,4),Q(1,2)]]]
    require(compatible(good),'valid occupation array')
    nonzero=next((x,f) for x,f in good[0] if x)
    recovered=tuple(a/nonzero[0] for a in nonzero[1])
    require(recovered==u,'zero-safe reconstruction')
    impossible=[[(Q(1,2),(Q(1,2),Q(0))),(Q(1,2),(Q(0),Q(1,2)))]]
    require(not compatible(impossible),'hidden-environment row must be rejected')
    different_times=[[(Q(1),(Q(1,4),Q(3,4)))],[(Q(1),(Q(3,4),Q(1,4)))]]
    require(compatible(different_times),'clocked independent rows are legal')
    require(not compatible(different_times,shared=True),'autonomous shared-row violation')
    # An exact level-one dual identity for a blind binary decision.
    for q in (Q(i,7) for i in range(8)):
        for v in (Q(0),Q(1,3),Q(1,2)):
            require(Q(1,2)-v == ((1-q-v)+(q-v))/2,'blind-test dual polynomial identity')
    m,k,d=8,3,4
    calibration=(m+1) if MUTANT=='unpriced-calibration' else (m+1)**k
    require(calibration==729 and 3*d*calibration==8748,'persistent calibration vector')
    exact_dyadic = (Q(2,3).denominator & (Q(2,3).denominator-1))==0
    if MUTANT=='fair-bit-exact':
        exact_dyadic=True
    require(not exact_dyadic,'2/3 is not a bounded fair-bit probability')
    return {'schema':'gtf23.finite-checks/1','checks':CHECKS,**counts,
            'arithmetic':'exact rational; no floating point optimizer',
            'examples':examples,'symbolic_certificate':'three-report-frontier.tex: eq:v23-gap-certificate',
            'stochastic_grid_is_not_a_continuum_proof':True,
            'analytic_proofs_independently_verified':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant',choices=['minimax-as-bayes','wrong-terminal-denominator',
            'drop-minors','shared-row-free','unpriced-calibration','fair-bit-exact','wrong-roc-order'])
    MUTANT=parser.parse_args().mutant
    print(json.dumps(run(),indent=2,sort_keys=True))
