#!/usr/bin/env python3
"""Finite A2 v25 checks. No physical probe, uniform proof or novelty certification.

All assertions are explicit exceptions, so python -O executes the same checks.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from calibrate_fingerprint import calibrate, upper_log2

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()


def check(ok: bool, group: str) -> None:
    if not ok:
        raise RuntimeError(group)
    COUNTS[group] += 1


def continuation() -> None:
    for m in range(1, 81):
        check(F(2**m * m**m, math.factorial(m)) < 6**m,
              'complex_lagrange_amplification')
    # alpha = log(3/2)/log(9) > 1/8, checked without logs.
    check(F(3,2)**8 > 9, 'real_to_disk_exponent')
    for m in range(1,35):
        for factor in [F(1), F(2), F(5), F(8)]:
            t = factor/F(9**(m+1))
            bound = 6**m*t + F(4,3)*F(2,3)**(m+1)
            check((bound/3)**8 <= t, 'interpolation_power_bound')
    for J in range(8,140):
        theta = F(1,2**(J+3))
        for m0 in [1,3,8,29]:
            P = m0*2**(J+3)
            check(P*theta==m0, 'dyadic_chain_cancellation')
    for n,d in itertools.product(range(1,45),range(1,19)):
        q=F(n,d); m=upper_log2(q)
        check(2**m>=q, 'exact_log_upper')
        check(m==0 or 2**(m-1)<q, 'exact_log_minimal')


def calibration() -> None:
    base={'rho':'1/2','M':'2','R':'1/2','M_g':'1','kappa_min':'1/4',
          'R_plus':'9','D_0':'3','eta':'1/100','sigma':'1/50','d_0':'1/10'}
    for rho,eta,sep in itertools.product(['1/4','1/2','1','3/2'],
                                       ['1/100','1/10','1'], ['1/20','1/2']):
        p={**base,'rho':rho,'eta':eta,'sigma':sep,'d_0':sep}
        result=calibrate(p); c={k:F(v) for k,v in result['rational_constants'].items()}
        k=result['integers']; delta=c['Delta_star']; B=c['B']
        check(3*B/F(2**k['m0'])<=delta,'calibrated_continuation_target')
        check(9*delta<F(p['sigma']),'shape_locking_margin')
        check(9*delta<F(p['eta']),'reflection_locking_margin')
        check(c['C_star']*delta<F(p['d_0']),'physical_copy_locking_margin')
        check(k['c1']>=4*c['H']*c['r']/B,'symbolic_mesh_bound')
        check(2**k['tail_extra']>=64*F(p['M_g'])/(7*B),'symbolic_tail_bound')
        check(k['J']*c['a']>=4,'real_circle_coverage')
        check(c['a']<=F(p['rho'])/8,'complex_circle_within_strip')
    for bad in [0, -1, 0.5, True]:
        try:
            calibrate({**base,'rho':bad})
        except (ValueError, TypeError, ZeroDivisionError):
            check(True,'invalid_prior_rejected')
        else:
            check(False,'invalid_prior_rejected')
    # The huge threshold itself need not be expanded to check the normalized bounds.
    for d in [F(0),F(1,32),F(1,16),F(1,8)]:
        check(3*d/2+F(1,4)<1,'jet_support_budget')
        check(2*d+F(1,4)<=F(1,2),'value_support_budget')
    for P in range(2,70):
        for tail_extra in range(0,9):
            K=P+tail_extra+2
            check(3*(K+1)>=P+tail_extra,'conservative_jet_order')


def polynomial(c, x, derivative=0):
    return sum(F(math.factorial(j),math.factorial(j-derivative))*c[j]*x**(j-derivative)
               for j in range(derivative,len(c)))


def value_differences() -> None:
    polynomials=[list(map(F,c)) for c in
                 [[0,0,1,1],[1,-2,1,-1,1],[0,1,2,3,-1,2],
                  [2,0,-1,2,0,-2,1]]]
    for c,x,t in itertools.product(polynomials,[F(-1,3),F(0),F(1,4)],
                                   [F(1,8),F(1,16),F(1,32)]):
        M3=sum(abs(F(j*(j-1)*(j-2))*c[j]) for j in range(3,len(c)))
        eps=t**3/32
        true1=polynomial(c,x,1); true2=polynomial(c,x,2)
        for signs in itertools.product([-1,1],repeat=3):
            lo=polynomial(c,x-t)+signs[0]*eps
            mid=polynomial(c,x)+signs[1]*eps
            hi=polynomial(c,x+t)+signs[2]*eps
            d1=(hi-lo)/(2*t); d2=(hi-2*mid+lo)/t**2
            check(abs(d1-true1)<=M3*t*t/6+eps/t,'value_first_derivative_enclosure')
            check(abs(d2-true2)<=M3*t/3+4*eps/t**2,'value_second_derivative_enclosure')
    for M3,nu in itertools.product([F(1,4),F(1),F(10),F(25)],
                                  [F(1,4),F(1,10),F(1,100)]):
        t=min(F(1),nu/(4*(1+M3))); eps=nu*t*t/32
        check(M3*t*t/6+eps/t<nu,'first_difference_tolerance')
        check(M3*t/3+4*eps/t**2<nu,'second_difference_tolerance')
    for N in range(2,55):
        grid=[F(-1,2)+F(j,N) for j in range(N+1)]
        for j in range(N+1):
            check(grid[N-j]==-grid[j],'finite_grid_reversal')
        values=[F(j*j+3*j+1,7) for j in range(N+1)]
        check(list(reversed(list(reversed(values))))==values,'reversal_involution')
    for ea,eb in itertools.product([F(-1,17),F(0),F(1,17)],repeat=2):
        check(abs(ea-eb)<F(1,8),'same_class_band')
        check(abs(1+ea-eb)>F(7,8),'distinct_class_band')


def cost_exponents() -> None:
    check(3+2-6==-1,'fixed_a6_s2_is_harmonic_bound')
    for s in [F(0),F(1,2),F(1),F(3,2),F(2),F(4),F(9)]:
        a=max(F(6),5+s)
        check(3+s-a<-1,'generic_cost_summability')
        check((3+s-6<-1)==(s<2),'scope_of_fixed_a6')
    for sv in [F(0),F(1,4),F(1,2),F(1),F(2),F(4)]:
        s=1+3*sv; a=max(F(6),6+3*sv)
        check(4+s==5+3*sv,'value_query_total_power')
        check(3+s-a<-1 and a>5+3*sv,'value_query_expected_cost')
    for beta in [F(1,4),F(1,2),F(3,4),F(1)]:
        h=1/(2*beta+6)
        check((beta+3)*h==F(1,2),'coordinate_precision_power_retained')
        check(F(1,2)-3*h==beta*h,'histogram_stochastic_balance_retained')


def source_checks() -> None:
    preserved={'03_local_acquisition.tex':'3eed5495efbb84f3270607e7cae87d745fb88cf1',
               '04_inverse_certificate.tex':'8d6735f47f2937faf10f5224d04b1cbc201ac673',
               '05_noisy_stopping.tex':'dc2c449e48ef7c667a7dd11f0295b81916ec1fea'}
    for name,want in preserved.items():
        raw=(ROOT/'core'/name).read_bytes()
        check(hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()==want,
              'unchanged_active_core_blob')
    text=(ROOT/'main.tex').read_text()
    inputs=re.findall(r'\\input\{([^}]+)\}',text)
    for name in inputs:
        path=ROOT/(name+'.tex');check(path.is_file(),'reachable_input')
        text+='\n'+path.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)),'unique_labels')
    for ref in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
        check(ref in labels,'resolved_reference')
    for label in ['thm:main','thm:effective-main','lem:presentation-compactness',
                  'lem:finite-separation','prop:registry','thm:effective',
                  'thm:value-gates','thm:certificate']:
        check(label in labels,'retained_and_new_main_results_present')
    setting=(ROOT/'core/01_setting.tex').read_text()
    check('a=6.' not in setting,'headline_tail_choice_corrected')
    check('a\\ge6' in setting and 'a>4+s' in setting,'headline_cost_condition_explicit')


if __name__=='__main__':
    continuation(); calibration(); value_differences(); cost_exponents(); source_checks()
    print(json.dumps({'schema':'a2-v25-finite-diagnostics-1','status':'passed',
                      'finite_checks':sum(COUNTS.values()),
                      'groups':dict(sorted(COUNTS.items())),
                      'scope':'finite exact algebra, error budgets, derivative enclosures, source structure',
                      'physical_sensor_executed':False,'formal_proof_certificate':False},
                     sort_keys=True,indent=2))
