#!/usr/bin/env python3
"""Finite diagnostics for the A2 v10 addition; not a proof certificate.
Requires SymPy. No network, assertion-based checks, interval arithmetic,
physical probability oracle, or manuscript imports. Ordinary numerical
checks below concern integer design rounding, not simulated billiards.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_V9_COUNT = 168
EXPECTED_V9_DIGEST = '8eaec7e57da29cad14396fec82418ebd413f1359e013086f44929d28d3e77447'
V9_INPUTS = ['main.tex', 'preamble.tex', 'article/01_introduction.tex', 'article/02_finite_results.tex', 'v3/10_geometry_action.tex', 'v3/20_integration.tex', 'v4/10_boundary_layers.tex', 'v5/15_differentiated_operators.tex', 'v4/20_nonlinear_information.tex', 'article/15_operator_comparison.tex', 'article/20_boundary_compatibility.tex', 'v6/10_experiment_transfer.tex', 'v7/10_critical_experiments.tex', 'article/30_supercritical.tex', 'v3/40_inverse.tex', 'v5/40_pairwise_inverse.tex', 'v6/30_three_amplitudes.tex', 'article/40_fixed_offset.tex', 'article/50_joint_minimax.tex', 'article/60_smooth_remainders.tex', 'article/65_envelope_minimax.tex', 'article/70_comparison.tex', 'v5/20_contact_rigidity.tex', 'v6/20_finite_jet_stability.tex', 'v3/30_observability.tex', 'v4/30_saturation_acquisition.tex', 'v5/50_self_calibration.tex', 'v4/40_coalescence.tex', 'v7/20_measurable_reconstruction.tex', 'v6/40_count_only_acquisition.tex', 'v7/30_count_lower_bounds.tex', 'v7/40_fixed_bracket_acquisition.tex', 'article/90_marked_results.tex', 'v3/50_record_response.tex', 'v3/circular_results.tex', 'sections/02_flux.tex', 'sections/03_geometry.tex', 'v3/circular_action.tex', 'sections/05_threshold_proof.tex', 'sections/06_records.tex', 'sections/07_consequences.tex', 'v5/references.tex']
CHECKS = []

def check(name, value, kind='exact_algebra'):
    if not value:
        raise RuntimeError('Failed: ' + name)
    CHECKS.append({'name': name, 'kind': kind, 'status': 'pass'})

def exact(name, expression):
    check(name, S.cancel(S.expand(expression)) == 0)

def sources(rel='main.tex', stack=()):
    if rel in stack:
        raise RuntimeError('Cyclic input: ' + rel)
    text = (ROOT/rel).read_text(encoding='utf-8')
    result = [(rel, text)]
    for name in re.findall(r'\\input\{([^}]+)\}', text):
        result += sources(name+'.tex', stack+(rel,))
    return result

def run():
    u = S.symbols('u')
    # Exact reproduction on the finitely many endpoint/interior stencil types.
    seen = set()
    for m in (4, 5, 6):
        L = m+4
        for ell in range(L):
            start = max(1, min(ell, L-m+1))
            absolute = list(range(start, start+m))
            nodes = tuple(k-ell for k in absolute)
            check(f'positive_in_collar_{m}_{ell}', min(absolute)>=1 and max(absolute)<=L)
            check(f'bounded_stencil_span_{m}_{ell}', max(abs(k) for k in nodes)<=m)
            key = (m, nodes)
            if key in seen:
                continue
            seen.add(key)
            basis = [S.prod((u-v)/(w-v) for v in nodes if v!=w) for w in nodes]
            for power in range(m):
                poly = S.expand(sum(w**power*p for w,p in zip(nodes,basis)))
                check(f'monomial_and_three_derivatives_{m}_{nodes}_{power}',
                      all(S.expand(S.diff(poly-u**power,u,r))==0 for r in range(4)))
            # The cubic data bias has bounded third derivative on every stencil.
            exact(f'cubic_bias_not_h_amplified_{m}_{nodes}',
                  S.diff(sum(w**3*p for w,p in zip(nodes,basis)),u,3)-6)
    # Bernstein algebra, including scaling of an unconditioned Bernoulli report.
    a,M,t,N,p = S.symbols('a M t N p', positive=True)
    F = a*p
    exact('scaled_bernoulli_variance',a*a*p*(1-p)/N-a*F*(1-p)/N)
    s = t/(M+t/3)
    exponent = -N*s*t/a + N*(M/a)*s*s/(2*(1-s/3))
    exact('bernstein_exponential_parameter',exponent+N*t*t/(2*a*(M+t/3)))
    for n in range(2,16):
        check(f'exponential_series_coefficient_{n}', S.factorial(n)>=2*3**(n-2))
    eps,h,gamma,lam = S.symbols('eps h gamma lam', positive=True)
    exact('mesh_sampling_power',h**(-2)*(eps*h**3)**(-2)-eps**(-2)*h**(-8))
    for m in range(4,11):
        exact(f'total_preparation_exponent_{m}',
              2+S.Rational(2,m-3)+S.Rational(6,m-3)+gamma/lam
              -(2+S.Rational(8,m-3)+gamma/lam))
        check(f'ceiling_term_is_lower_order_{m}',
              2+S.Rational(8,m-3)>S.Rational(1,m-3))
    # Direct beta normalization and a polynomial full-collar law, not a table realization.
    x,y,d,c0,c1 = S.symbols('x y d c0 c1')
    def coefficient(r,s):
        return 2*S.rf(S.Rational(1,2),r)*S.rf(S.Rational(1,2),s)/S.factorial(r+s+2)
    exact('positive_simplex_mass',coefficient(0,0)-1)
    law = sum(coefficient(r,s)*c0**r*c1**s*d**(r+s) for r in range(2) for s in range(2))
    exact('linear_profile_full_law',law-(1+(c0+c1)*d/6+c0*c1*d*d/48))
    # Ordinary floating-point diagnostics of even rounding in the stated design.
    for tau in (.25,.6,.85):
        for gamma_value in (.4,1.3):
            for accuracy in (1e-2,1e-4,1e-7):
                c=.01
                j=max(2,2*math.ceil(math.log(c*accuracy)/math.log(tau)/2))
                check(f'even_rounding_bias_{tau}_{gamma_value}_{accuracy}',
                      j%2==0 and tau**j<=c*accuracy*(1+1e-12),'ordinary_float')
                bound=math.exp(2*gamma_value)*(c*accuracy)**(-gamma_value/abs(math.log(tau)))
                check(f'even_rounding_cost_{tau}_{gamma_value}_{accuracy}',
                      math.exp(j*gamma_value)<=bound*(1+1e-12),'ordinary_float')
    # Byte retention: every original v9 formal environment, in original source order.
    active=sources();names=[n for n,_ in active]
    check('all_v9_inputs_still_active',set(V9_INPUTS)<=set(names),'source_integrity')
    old=[(n,s) for n,s in active if n in set(V9_INPUTS)]
    check('v9_input_order_preserved',[n for n,_ in old]==V9_INPUTS,'source_integrity')
    pattern=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}',re.S)
    blocks=[m.group(0).encode() for _,text in old for m in pattern.finditer(text)]
    digest=hashlib.sha256(b''.join(str(len(b)).encode()+b'\0'+b for b in blocks)).hexdigest()
    check('all_v9_formal_blocks_byte_identical',len(blocks)==EXPECTED_V9_COUNT and digest==EXPECTED_V9_DIGEST,'source_integrity')
    text='\n'.join(s for _,s in active)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check('unique_labels',len(labels)==len(set(labels)),'source_integrity')
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text)
    check('resolved_internal_references',all(r in labels or r.startswith('TC-') for r in refs),'source_integrity')
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    cites={k.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in group.split(',')}
    check('resolved_bibliography',cites<=keys,'source_integrity')
    check('focused_inverse_references_present',{'DaiLamm','HofmannWernerDeng'}<=keys,'source_integrity')
    check('new_acquisition_and_budget_present',{'thm:v10-acquisition','cor:v10-budget'}<=set(labels),'source_integrity')
    return {'schema':'a2-v10-finite-diagnostics-v1','status':'pass',
            'counts':{'total':len(CHECKS),**dict(Counter(c['kind'] for c in CHECKS))},
            'checks':CHECKS,
            'source_retention':{'original_v9_formal_environments':len(blocks),
                                'ordered_length_prefixed_sha256':digest,
                                'all_byte_identical':True,
                                'current_formal_environments':len(list(pattern.finditer(text)))},
            'limitations':['Finite diagnostics are not formal proofs of the written analytical or statistical theorems.',
                           'Ordinary floating-point rounding checks are not interval enclosures.',
                           'No exact nonlinear finite-offset billiard probabilities or physical simulations were used.',
                           'The preparation upper bound does not control dictionary size or computational complexity.',
                           'Retained-environment counts are source-integrity evidence, not numbers of certified theorems.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'verification/v10_diagnostics.json')
    args=parser.parse_args();result=run();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'counts':result['counts'],'source_retention':result['source_retention']},sort_keys=True))
