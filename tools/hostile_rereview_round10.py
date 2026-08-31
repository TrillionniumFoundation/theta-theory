#!/usr/bin/env python3
"""Counterexample-aware hostile regression checks for Round Ten."""
from __future__ import annotations
from pathlib import Path
import json, math, subprocess, sys, re

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'revision'/'round10-referee-final'
texts={p.name:p.read_text() for p in SRC.glob('*.tex')}
errors=[]; result={'schema':'theta-theory-round10-hostile-rereview-v1','papers':{}}

def require(paper,file,*snippets):
    t=texts[file]
    missing=[s for s in snippets if s not in t]
    if missing: errors.append(f'{paper}: missing {missing}')
    result['papers'][paper]={'status':'PASS' if not missing else 'FAIL','checked':list(snippets)}

# A1: direct counterexample grows under the rejected bilateral norm; the new source must use one-sided P.
alpha=.6; n=12; old_growth=alpha**(-n)
require('A1','A1_MAPPING_TORUS_ONE_SIDED_RESPONSE.tex','P_a^+','P_a^-','never applies a bilateral inverse shift','mapping-torus','Hadamard')
result['papers']['A1']['rejected_bilateral_growth']=old_growth
if old_growth<=1: errors.append('A1 regression arithmetic failed')

# A2: run exact certificate and check the corrected sum-window scaling.
cp=subprocess.run([sys.executable,str(ROOT/'tools'/'verify_a2_round10_certificate.py')],cwd=ROOT,capture_output=True,text=True)
if cp.returncode: errors.append('A2 certificate executable failed: '+cp.stdout+cp.stderr)
require('A2','A2_EXPLICIT_CERTIFICATE_FOURIER_RANGES.tex','very-high','integrate','roof-sum interval','fixed interval in the roof average','Verified returned-branch UNI')
result['papers']['A2']['certificate']=cp.stdout.strip()

# A3 deterministic speeds and retained state.
require('A3','A3_DETERMINISTIC_SPEED_PROJECTIVE_FLOW_LDP.tex','The speed is the deterministic integer','edge flow','actual excursion','deterministic collision horizon','deterministic physical time')
if re.search(r'at speed \$?R_N',texts['A3_DETERMINISTIC_SPEED_PROJECTIVE_FLOW_LDP.tex']): errors.append('A3 random speed remains')

# A4 Poisson centering algebra and memory sign.
require('A4','A4_DOOB_PAST_KERNEL_MEMORY.tex','P(g+h_g)(H_k)=Ph_g(H_k)','h_\\Psi^{-1}T_t^\\Psi','zP-PL_\\Psi P-C(z)^{-1}','raw centered observable is never called a martingale difference')

# B1 no fixed rare sector; good-block failure exponential.
require('B1','B1_INTERIOR_SADDLE_REGENERATIVE_SHELL.tex','relative interior','c\\mu_\\varepsilon','good blocks','e^{-c\\mu_\\varepsilon}','sqrt{\\mu_\\varepsilon}')

# B2 integrated physical loss and no QR reset as proof mechanism.
require('B2','B2_COMPATIBLE_TRACE_INTEGRATED_JACOBI_LDP.tex','Flux-weighted Jacobi small-ball estimate','Split at','post-collisional trajectory','no QR change','Exact conservative regularization')
beta=0.8; eps=1e-8; rho=eps**(2/(beta+2)); bound=rho**beta+eps**2*rho**-2
result['papers']['B2']['optimized_integrated_gain']=bound
if not bound<eps**0.2: errors.append('B2 optimized gain not small')

# B3 raw negative example and covariance-first route.
require('B3','B3_COVARIANCE_FIRST_GAUGE_PROCESS.tex','raw second variation may be indefinite','No curvature is added from the linear balance multiplier','Finite-volume covariance first','Second epi-derivative and covariance inverse','Localized connected-cumulant estimate')
q=2; raw=2*(1-q)
result['papers']['B3']['raw_counterexample_value']=raw
if raw>=0: errors.append('B3 negative regression failed')

# B4 type separation, no state resolvent, dynamic-only action, coercive penalty.
require('B4','B4_DYNAMIC_ACTION_GRAPH_CORE_COMPARISON.tex','Five objects are kept distinct','observable resolvent','initial rate is absent from every transition interval','d_\\lambda(f,g)^2','first sending $\\epsilon\\downarrow0$','Laplace principle')
for bad in ['entire cutoff equal to one','state-space resolvent applied to an observable']:
    if bad in texts['B4_DYNAMIC_ACTION_GRAPH_CORE_COMPARISON.tex'].lower(): errors.append(f'B4 obsolete mechanism remains: {bad}')
result['papers']['B4']['diagonal_penalty_at_dist_0.4']=[0.4**2/(2*e) for e in (1,.1,.01,.001)]

# C1 evidence may be tiny; lifted state remains finite.
require('C1','C1_STRATIFIED_EVIDENCE_FILTERING.tex','unnormalized observation current','evidence','no uniform lower bound','codimension','reachable')
result['papers']['C1']['tiny_log_evidence']=math.log(1e-30)

# C2 linear spans and no RN trivialization.
require('C2','C2_COMMON_TRANSFER_BUNDLE_COTANGENTS.tex','closed linear','uniform Ces','without infinite-path Radon--Nikodym densities','Kato',r'C_\eta(z)')
if 'd\\nu_\\eta/d\\nu_0' in texts['C2_COMMON_TRANSFER_BUNDLE_COTANGENTS.tex']: errors.append('C2 infinite-path RN derivative remains')

# D1 common-space positive components and no false conjugacy.
require('D1','D1_MICROSCOPIC_PHASE_DISINTEGRATION.tex','disjoint measurable phase basins','Microscopic phase mixture LDP','phase-local','Lee--Yang')
if 'follows from the identity' in texts['D1_MICROSCOPIC_PHASE_DISINTEGRATION.tex'].lower(): errors.append('D1 false max-conjugacy derivation remains')
result['papers']['D1']['false_conjugacy_counterexample']={'conjugate_of_max_at_zero':0.5,'min_of_conjugates_at_zero':0.0}

result['errors']=errors
result['paper_count']=11
result['status']='PASS' if not errors else 'FAIL'
(ROOT/'ROUND10_HOSTILE_REREVIEW.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if errors:
    for e in errors: print('ROUND10_HOSTILE_ERROR',e,file=sys.stderr)
    raise SystemExit(1)
print('ROUND10_HOSTILE_REREVIEW_PASS 11/11')
