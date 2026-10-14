#!/usr/bin/env python3
"""Finite algebra/model checks only; independent of the proof source and solvers."""
from __future__ import annotations
from fractions import Fraction as F
import json
import math


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def main() -> None:
    checks = 0
    # Exact Palm and length-bias bookkeeping on a periodic suspension.
    roofs = [2, 3, 5]
    marks = [1, 4, 8]
    period = sum(roofs)
    starts = [0, 2, 5]
    grid = 20
    for t in range(1, 13):
        for q in range(10):
            visit_sum = F(0)
            max_count = 0
            events = []
            for k in range(period*grid):
                phase = F(2*k+1,2*grid)
                current = max(i for i,s in enumerate(starts) if s < phase)
                hit = marks[current] > q
                count = 0
                for lap in range(-1,4):
                    for i,start in enumerate(starts):
                        when = F(start+lap*period)-phase
                        if 0 < when <= t:
                            count += int(marks[i] > q)
                            hit = hit or marks[i] > q
                visit_sum += count
                max_count += int(hit)
                events.append(hit)
            expectation = visit_sum/(period*grid)
            require(expectation == F(t*sum(m>q for m in marks),period), 'marked Palm identity')
            init = F(sum(r for r,m in zip(roofs,marks) if m>q),period)
            bound = init + expectation
            require(F(max_count,period*grid) <= bound, 'stationary maximum union bound')
            for stride in (2,3,7):
                selected = list(range(0,len(events),stride))
                d = F(len(selected),len(events))
                conditional = F(sum(events[i] for i in selected),len(selected))
                require(conditional <= min(F(1),F(max_count,len(events))/d), 'rare-event division')
                checks += 1
            checks += 2
    # Two-state dependent Markov model: soft killing and its eigenvalue derivative.
    P = ((0.8,0.2),(0.3,0.7))
    def eigen(z):
        x=math.exp(-z)
        tr=P[0][0]+P[1][1]*x
        det=(P[0][0]*P[1][1]-P[0][1]*P[1][0])*x
        return (tr+math.sqrt(tr*tr-4*det))/2
    eps=1e-6
    require(abs((eigen(eps)-eigen(-eps))/(2*eps)+0.4)<1e-8,'eigenvalue derivative equals minus mean')
    checks += 1
    for z in (0.0001,0.001,0.01):
        require(eigen(z) <= 1-0.2*z,'small positive killing contracts')
        row=[0.6,0.4]
        for n in range(1,101):
            x=math.exp(-z)
            row=[row[0]*P[0][0]+row[1]*x*P[1][0],row[0]*P[0][1]+row[1]*x*P[1][1]]
            require(0 < sum(row) <= 2*eigen(z)**n,'finite killed expectation')
            checks += 1
        checks += 1
    # Exact exponent cancellation and improved one-step radius inequalities.
    for alpha in (F(1),F(1,2),F(1,4)):
        for zeta in (F(0),F(1,2),F(2)):
            for p in (1,2,4):
                lam = F(2,p)*max(F(1),zeta/alpha)
                old = F(2,p)*(F(1)+max(F(1),zeta/alpha))
                require(lam < old,'no full-period geometric exponent')
                require(1+F(2,p)/alpha >= 1+F(2,p),'logarithmic loss budget')
                checks += 2
    for B in (1,2,10,100):
        # q(t)=exp(-|t|): L1=2; total variation of D2 q is 4.
        exact=4*math.atan(1/B)
        require(exact <= 8/B,'absolute second-derivative Fourier tail')
        checks += 1
    print(json.dumps({'status':'passed','checks':checks,
        'scope':'finite rational suspension, finite Markov model, exponent algebra, explicit Fourier example',
        'continuum_spectral_theorem_verified_by_tests':False,
        'all_parameter_billiard_proofs_are_in':'core/15_exponential_returns.tex and core/18_conditioned_clock.tex',
        'full_raw_LLT_verified':False,'independent_human_review':False},indent=2))

if __name__ == '__main__':
    main()
