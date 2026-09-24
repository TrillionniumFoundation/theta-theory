#!/usr/bin/env python3
"""Exact reproducibility checks, not a substitute for analytic proofs.

No assert statements: all checks remain active under python -O.
No floating-point optimization or parameter grid is used for the main bounds.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import sympy as sp

COUNT = 0

def require(condition: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutant', choices=['certificate', 'selector', 'polynomial', 'profile', 'shared-row', 'autonomous'])
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    Q = [F(5,16), F(3,16), F(3,16), F(5,16)]
    weights = [F(1,16), F(7,16), F(7,16), F(1,16)]
    points = [F(1,8), F(1,5), F(4,5), F(7,8)]
    require(sum(weights) == 1, 'prior normalization')
    numerators = [[-1977,-1775177,2170423,3943623],
                  [1765554,191954,191954,1765554],
                  [3943623,2170423,-1775177,-1977]]
    if args.mutant == 'certificate':
        numerators[0][0] += 1
    table = []
    for k in range(3):
        row = []
        for j in range(4):
            coefficient = sum(w*comb(2,k)*p**k*(1-p)**(2-k)
                *(Q[j]-((1-p)**2 if j < 2 else p**2)/2)
                for w,p in zip(weights,points))
            require(coefficient == F(numerators[k][j],40960000), 'one-preparation certificate coefficient')
            row.append(coefficient)
        table.append(row)
    upper = sum(max(F(0),a) for row in table for a in row)
    require(upper == F(4035777,10240000), 'positive-part sum')
    gap = F(2,5)-upper-F(1,300)
    require(gap == F(78269,30720000) and gap > 0, 'physical exclusion margin')
    require(F(27,64)-F(1,300) > F(2,5), 'rational construction margin')

    rows = [(0,0,1,1),(1,0,1,1),(1,1,1,1),(1,1,0,1),(1,1,0,0)]
    if args.mutant == 'selector':
        rows[0] = (1,0,1,1)
    p,q,u,v = sp.symbols('p q u v')
    a,c = (1-p)*(1-q),p*q
    G = 0
    for k in range(3):
        for ell in range(3):
            likelihood = comb(2,k)*p**k*(1-p)**(2-k)*comb(2,ell)*q**ell*(1-q)**(2-ell)
            score = sum((sp.Rational(t.numerator,t.denominator)-b)*h
                        for t,b,h in zip(Q,[a/2,a/2,c/2,c/2],rows[k+ell]))
            G += likelihood*score
    H = (-u**3+3*u**2*v+6*u**2-3*u*v**2-8*u*v-3*u
         +v**3+2*v**2+15*v+14)/32
    if args.mutant == 'polynomial':
        H += sp.Rational(1,100)
    require(sp.expand(G-H.subs({u:(p+q-1)**2,v:(p-q)**2})) == 0, 'two-preparation polynomial identity')
    require(sp.expand(32*sp.diff(H,v)-(3*(u-v)**2-8*u+4*v+15)) == 0, 'nonnegative transverse derivative')
    require(sp.expand(32*sp.diff(H,v)-7-(3*(u-v)**2+8*(1-u)+4*v)) == 0, 'transverse derivative lower bound')
    m2 = (12-3*sp.sqrt(3))/16
    require(sp.simplify(H.subs({v:0,u:2-sp.sqrt(3)})-m2) == 0, 'exact minimum value')
    require(sp.expand(32*sp.diff(H.subs(v,0),u)-(-3*u**2+12*u-3)) == 0, 'critical point derivative')
    require(sp.Rational(7,4)**2 > 3, 'rational radical comparison')

    def value(word: tuple[int,...]) -> int:
        s = sum(word[i] for i in (0,1,3,4))
        row = rows[s]
        def event(offset: int) -> int:
            x,y,w = word[offset:offset+3]
            return row[2*x+w] if x == y else 0
        return event(9)-event(6)

    residuals = [None]*13
    residuals[12] = {word:(value(word),) for word in product((0,1),repeat=12)}
    for t in range(11,-1,-1):
        residuals[t] = {word:residuals[t+1][word+(0,)]+residuals[t+1][word+(1,)]
                        for word in product((0,1),repeat=t)}
    profile = [len(set(level.values())) for level in residuals]
    expected_profile = [1,2,3,3,4,5,5,10,12,10,10,7,3]
    if args.mutant == 'profile':
        expected_profile[8] = 10
    require(profile == expected_profile, 'full bit-level profile')
    require(sum(profile) == 75 and max(profile) == 12, 'peak and phase-tagged state costs')
    states = []
    for level in residuals:
        index = {r:i for i,r in enumerate(sorted(set(level.values())))}
        states.append({word:index[r] for word,r in level.items()})
    transitions = []
    for t in range(12):
        step = {}
        for word,state in states[t].items():
            destinations = [states[t+1][word+(bit,)] for bit in (0,1)]
            if state in step:
                require(step[state] == destinations, 'residual quotient shift compatibility')
            step[state] = destinations
        transitions.append([step[i] for i in range(profile[t])])
    output_values = [r[0] for r in sorted(set(residuals[12].values()))]
    for word in product((0,1),repeat=12):
        state = states[0][()]
        for t,bit in enumerate(word):
            state = transitions[t][state][bit]
        require(output_values[state] == value(word), 'compiled audit disagrees on a complete word')

    # One stochastic row is reused three times. The degree-three Bernstein
    # coefficients of a signed parity reward are mixed vertex products,
    # not a free mixture of the endpoint machines.
    lo,hi = F(1,4),F(3,8)
    coefficients = [(1-2*lo)**(3-k)*(1-2*hi)**k for k in range(4)]
    if args.mutant == 'shared-row':
        coefficients[1] = (1-2*lo)**3
    for j in range(9):
        lam = F(j,8)
        actual = (1-2*((1-lam)*lo+lam*hi))**3
        represented = sum(comb(3,k)*lam**k*(1-lam)**(3-k)*coefficients[k] for k in range(4))
        require(actual == represented, 'shared-row Bernstein reconstruction')
    for coefficient in coefficients:
        require(abs(coefficient-(1-2*lo)**3) <= F(6,8), 'causal HS/m bound')

    stationary_cases = 0
    for W in range(2,8):
        D = W-1
        for p0 in (F(1,4),F(1,3)):
            q0,r,eps = 1-p0,(1-p0)/p0,F(1,8)
            cw = [F(1)]+[eps]*(W-2)+[F(1)]
            laws = []
            for plus in (False,True):
                s = r if plus else 1/r
                weights_s = [cw[i]*s**i for i in range(W)]
                pi = [x/sum(weights_s) for x in weights_s]
                matrix = [[F(0) for _ in range(W)] for _ in range(W)]
                for i in range(W):
                    if i < D:
                        matrix[i][i+1] = (q0 if plus else p0)*min(F(1),cw[i+1]/cw[i])/2
                    if i > 0:
                        matrix[i][i-1] = (p0 if plus else q0)*min(F(1),cw[i-1]/cw[i])/2
                    matrix[i][i] = 1-sum(matrix[i])
                    require(matrix[i][i] >= F(1,2), 'autonomous holding probability')
                if args.mutant == 'autonomous':
                    pi[0] += F(1,100)
                require(sum(pi) == 1, 'stationary law normalization')
                for j in range(W):
                    require(sum(pi[i]*matrix[i][j] for i in range(W)) == pi[j], 'stationary detailed balance')
                decision = [F(0) if 2*i < D else F(1) if 2*i > D else F(1,2) for i in range(W)]
                error = sum(pi[i]*(1-decision[i] if plus else decision[i]) for i in range(W))
                require(F(1)/(1+r**D) <= error <= F(1)/(1+r**D)+eps*(W-2), 'autonomous approximation interval')
                laws.append(error)
            require(laws[0] == laws[1], 'equal autonomous errors')
            stationary_cases += 1

    result = {'schema':'gtf24.exact-checks/1','checks':COUNT,
              'one_trial_upper':str(upper),'one_trial_margin_at_two_fifths':str(gap),
              'two_trial_minimum':'(12-3*sqrt(3))/16','profile':profile,
              'complete_input_words':4096,'autonomous_phase_tagged_states':75,
              'autonomous_stationary_cases':stationary_cases,
              'polynomial_identity_exact':True,'coefficient_table_exact':True,
              'continuum_claims_proved_in_manuscript_not_by_grid':True}
    if args.output_dir:
        args.output_dir.mkdir(parents=True,exist_ok=True)
        machine = {'schema':'gtf24.deterministic-audit/1','event_rows':rows,
                   'profile':profile,'initial_state':states[0][()],
                   'transition_tables':transitions,'output_values':output_values,
                   'one_trial_coefficients':[[str(a) for a in row] for row in table]}
        (args.output_dir/'EXACT_MACHINE.json').write_text(json.dumps(machine,indent=2)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
