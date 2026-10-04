#!/usr/bin/env python3
"""Finite exact and numerical checks; not proof or physical sensor certification."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path
import re
import adaptive_scalar as a

CHECKS: Counter[str] = Counter()


def require(ok: bool, group: str) -> None:
    if not ok:
        raise RuntimeError(group)
    CHECKS[group] += 1


def interval_tests() -> None:
    for depth in range(1, 9):
        for bound in range(1, 5):
            inside = lambda p: -bound <= p[0] <= bound and -bound <= p[1] <= bound
            forcing = {p: a.Interval(F((p[0] * 7 + p[1] * 3) % 13 - 6, 11),
                                     F((p[0] * 7 + p[1] * 3) % 13 - 6, 11))
                       for p in a.diamond(depth - 1) if inside(p)}
            exact = a.local_interval(forcing, depth, inside, F(0))['iterate']
            # Independent full-square update with explicit killed rows.
            square = list(itertools.product(range(-bound, bound + 1), repeat=2))
            u = dict.fromkeys(square, F(0))
            for _ in range(depth):
                u = {p: min(F(1), max(F(0), sum((u.get((p[0]+i,p[1]+j),F(0))
                       for i,j in a.SHIFTS),F(0))/4-F((p[0]*7+p[1]*3)%13-6,11))) for p in square}
            require(exact.lower == exact.upper == u[(0, 0)], 'dependency_diamond_equals_killed_square')
            for error in (F(1, 100), F(1, 50)):
                intervals = {p: a.Interval(g.lower-error, g.upper+error) for p,g in forcing.items()}
                enclosed = a.local_interval(intervals,depth,inside,F(0))['iterate']
                require(enclosed.lower <= exact.lower <= enclosed.upper,'interval_encloses_exact_iterate')
                require(exact.lower-enclosed.lower <= depth*error and
                        enclosed.upper-exact.upper <= depth*error,'forcing_error_accumulation')
    for depth in range(1, 13):
        occ = lambda p: F(p in ((0,0),(1,0)))
        inside = lambda p: -3 <= p[0] <= 4 and -3 <= p[1] <= 3
        forcing = {}
        for p in a.diamond(depth-1):
            if inside(p):
                g=sum((occ((p[0]+i,p[1]+j)) for i,j in a.SHIFTS),F(0))/4-occ(p)
                forcing[p]=a.Interval(g,g)
        result=a.local_interval(forcing,depth,inside,F(1,4**depth))
        require(result['iterate'].lower==1-F(1,4**depth),'two_site_compass_survival')
        require(result['occupation'].lower <= 1 <= result['occupation'].upper,'conditional_occupation_enclosure')


def bisection_tests() -> None:
    for boundary in [F(k,32) for k in range(1,32)]:
        for ambiguity in [F(0),F(1,64),F(1,16)]:
            states={(F(0),F(1))}
            for depth in range(1,9):
                nxt=set()
                for lo,hi in states:
                    mid=(lo+hi)/2
                    permitted=[]
                    if mid<=boundary+ambiguity:permitted.append(True)
                    if mid>=boundary-ambiguity:permitted.append(False)
                    for bit in permitted:
                        l,u=(mid,hi) if bit else (lo,mid)
                        require(l-ambiguity<=boundary<=u+ambiguity,'adversarial_relaxed_bracket')
                        require(abs((l+u)/2-boundary)<=ambiguity+F(1,2**(depth+1)),
                                'adversarial_radius_error')
                        nxt.add((l,u))
                states=nxt
    for phase in range(12):
        boundary=F(7,13); ambiguity=F(1,50); calls=[]
        def label(x):
            calls.append(x)
            if x<boundary-ambiguity:return True
            if x>boundary+ambiguity:return False
            return (len(calls)+phase)%2==0
        box=a.fuzzy_bisect(label,F(0),F(1),ambiguity,15)
        require(box.lower<=boundary<=box.upper,'bisection_callback_enclosure')
        require(len(calls)==15,'bisection_query_cap')


def interpolation_tests() -> None:
    for x in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
        for derivative in range(4):
            weights=a.lagrange_weights(x,derivative)
            for power in range(7):
                got=sum((w*F(j)**power for j,w in zip(range(-3,4),weights)),F(0))
                expected=F(0) if power<derivative else F(math.factorial(power),math.factorial(power-derivative))*x**(power-derivative)
                require(got==expected,'seven_node_polynomial_derivative_reproduction')
    for x in [F(0),F(1,3),F(2,3),F(1)]:
        for derivative in range(4):
            w=a.lagrange_weights(x,derivative);bound=sum(abs(v) for v in w)
            for signs in itertools.product([-1,1],repeat=7):
                require(abs(sum(v*t for v,t in zip(w,signs)))<=bound,'interpolation_extremal_noise')


def exponents_and_tree() -> None:
    for beta in (F(1,5),F(1,3),F(1,2),F(2,3),F(1)):
        s=6+beta; k=1/(s-2)
        require((s-2)*k==1,'C2_target_balance')
        require(s*k-2*k==1,'value_noise_derivative_balance')
        require(s-6==beta and s-2==4+beta,'physical_holder_packing_scale')
        require(k<3 and s*k< F(3,2),'comparison_with_uniform_grid_orders')
    for m in range(2,60):
        for n in range(m+1):
            require(F(2**n,2**m)>=F(3,4) if n==m else F(2**n,2**m)<F(3,4),
                    'binary_leaf_success_bound')
    for n in range(1,31):
        require(len(a.diamond(n))==1+2*n*(n+1),'dependency_center_count')


def numerical_radial() -> dict:
    rows=[]
    for m in (24,48,96):
        values=[2+.07*math.cos(2*2*math.pi*j/m)+.025*math.sin(3*2*math.pi*j/m) for j in range(m)]
        maxima=[0.,0.,0.]
        for j in range(71):
            t=2*math.pi*(j+.317)/71
            got=a.radial_interpolate(values,t)
            truth=(2+.07*math.cos(2*t)+.025*math.sin(3*t),
                   -.14*math.sin(2*t)+.075*math.cos(3*t),
                   -.28*math.cos(2*t)-.225*math.sin(3*t))
            for k in range(3):maxima[k]=max(maxima[k],abs(got[k]-truth[k]))
            require(got[0]**2+2*got[1]**2-got[0]*got[2]>1,'nonlinear_polar_convexity_margin')
        rows.append({'nodes':m,'errors_C0_C1_C2':maxima})
    for i in range(1,len(rows)):
        for k in range(3):
            require(rows[i]['errors_C0_C1_C2'][k]<rows[i-1]['errors_C0_C1_C2'][k]/8,
                    'nonlinear_radial_refinement')
    return {'scope':'floating_point_radial_examples_not_sensor_execution','runs':rows}


def source_checks() -> None:
    root=Path(__file__).resolve().parents[1]
    main=(root/'main.tex').read_text(); text=main
    for name in re.findall(r'\\input\{([^}]+)\}',main):
        p=root/(name+'.tex');require(p.is_file(),'active_input_exists');text+='\n'+p.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)),'unique_labels')
    for name in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):require(name in labels,'reference_resolved')
    for name in ('thm:adaptive','thm:lower','prop:query','lem:bisection','lem:radial','lem:locking','lem:packing','lem:bits'):
        require(name in labels,'main_proof_chain_present')
    for term in ('all-attempt','known positive','logarithmic gap','not a passive'):
        require(term.lower() in text.lower(),'information_scope_explicit')


def main() -> None:
    interval_tests(); bisection_tests(); interpolation_tests(); exponents_and_tree()
    numerical=numerical_radial();source_checks()
    print(json.dumps({'status':'passed','finite_checks':sum(CHECKS.values()),
                      'groups':dict(sorted(CHECKS.items())), 'numerical':numerical,
                      'formal_proof_certificate':False,'physical_sensor_executed':False},
                     indent=2,sort_keys=True))

if __name__=='__main__':main()
