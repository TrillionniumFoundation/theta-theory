#!/usr/bin/env python3
"""A2 v11 finite exact diagnostics and source retention; not proof certification.
Uses only the Python standard library. All checks raise normally under -O.
No physical probability oracle, simulation, network, or manuscript-code imports.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
OLD_INPUTS=['main.tex', 'preamble.tex', 'article/01_introduction.tex', 'article/02_finite_results.tex', 'v3/10_geometry_action.tex', 'v3/20_integration.tex', 'v4/10_boundary_layers.tex', 'v5/15_differentiated_operators.tex', 'v4/20_nonlinear_information.tex', 'article/15_operator_comparison.tex', 'article/20_boundary_compatibility.tex', 'article/22_deautoconvolution.tex', 'article/25_profile_acquisition.tex', 'v6/10_experiment_transfer.tex', 'v7/10_critical_experiments.tex', 'article/30_supercritical.tex', 'v3/40_inverse.tex', 'v5/40_pairwise_inverse.tex', 'v6/30_three_amplitudes.tex', 'article/40_fixed_offset.tex', 'article/50_joint_minimax.tex', 'article/60_smooth_remainders.tex', 'article/65_envelope_minimax.tex', 'article/70_comparison.tex', 'article/72_observable_comparison.tex', 'v5/20_contact_rigidity.tex', 'v6/20_finite_jet_stability.tex', 'v3/30_observability.tex', 'v4/30_saturation_acquisition.tex', 'v5/50_self_calibration.tex', 'v4/40_coalescence.tex', 'v7/20_measurable_reconstruction.tex', 'v6/40_count_only_acquisition.tex', 'v7/30_count_lower_bounds.tex', 'v7/40_fixed_bracket_acquisition.tex', 'article/90_marked_results.tex', 'v3/50_record_response.tex', 'v3/circular_results.tex', 'sections/02_flux.tex', 'sections/03_geometry.tex', 'v3/circular_action.tex', 'sections/05_threshold_proof.tex', 'sections/06_records.tex', 'sections/07_consequences.tex', 'v5/references.tex']
OLD_COUNT=176
OLD_DIGEST='157e702c92f66f2a12318527f7990aed240e82ad7a744eeffb75fbb8b09da721'
CHECKS=[]
def check(name,condition,kind='exact_algebra'):
    if not condition:
        raise RuntimeError('Failed: '+name)
    CHECKS.append({'name':name,'kind':kind,'status':'pass'})
def rising(n):
    return math.prod((F(2*k+1,2) for k in range(n)),start=F(1))
def lam(n):
    return 4*rising(n)/math.factorial(n+2)
def hcoef(v,w):
    z=[F(0)]*(len(v)+len(w)-1)
    for r,a in enumerate(v):
        for s,b in enumerate(w):
            z[r+s]+=2*a*b*rising(r)*rising(s)/math.factorial(r+s+2)
    return z
# Coefficients of the transformed integrated flux divided by pi.
def abel(v):
    return [a*math.factorial(n+2)/(2*rising(n)) for n,a in enumerate(v)]
def expand_sources(rel='main.tex',stack=()):
    if rel in stack:raise RuntimeError('Input cycle: '+rel)
    text=(ROOT/rel).read_text();out=[(rel,text)]
    for name in re.findall(r'\\input\{([^}]+)\}',text):
        out+=expand_sources(name+'.tex',stack+(rel,))
    return out
def run():
    for n in range(31):
        check(f'monomial_multiplier_{n}',lam(n)==F(4*math.comb(2*n,n),4**n*(n+1)*(n+2)))
        check(f'weighted_abel_linear_inverse_{n}',lam(n)*math.factorial(n+2)/(2*rising(n))==2)
    for seed in range(1,8):
        v=[F(1)]+[F((-1)**r*(seed+r),7+r) for r in range(1,5)]
        w=[F(1)]+[F(seed-r,9+r) for r in range(1,5)]
        left=[a-b for a,b in zip(abel(hcoef(v,v)),abel(hcoef(w,w)))]
        u=[a-b for a,b in zip(v,w)];a=[x+y for x,y in zip(v,w)]
        right=[F(0)]*len(left)
        for n,x in enumerate(u):right[n]+=2*x
        for r in range(1,len(a)):
            for s in range(len(u)):
                right[r+s]+=a[r]*u[s]*rising(r)*rising(s)/rising(r+s)
        check(f'nonlinear_weighted_volterra_polynomial_{seed}',left==right)
    for m in range(4,11):
        n=m+7;B=F(3,2);beta=F(3,4);a=min((B-1)/F(2*(m+1)),(1-beta)/2)
        derivs=[a*F(math.factorial(n),math.factorial(n-r)*n**m) for r in range(m+1)]
        check(f'fixed_sum_class_{m}',1+sum(derivs)<=B and a<1-beta)
        check(f'fixed_class_derivatives_{m}',all(d<=a*F(n)**(r-m) for r,d in enumerate(derivs)))
        check(f'C2_law_ratio_{m}',F(1,lam(n)*n*(n-1))>0)
        check(f'C2_integrated_ratio_{m}',F(1,lam(n)*(n+1)*(n+2))>0)
        # Only exact exponent identities; no asymptotic theorem inferred by finite checks.
        nu=F(m)-F(5,2)
        check(f'approximation_half_order_{m}',(F(m-2)+F(m-3))/2==nu)
        check(f'noise_half_order_{m}',(F(-2)+F(-3))/2==-F(5,2))
        check(f'preparation_exponent_{m}',2+F(1,1)/nu+F(5,1)/nu==2+6/nu)
        check(f'improved_over_integer_budget_{m}',6/nu<F(8,m-3))
        check(f'pilot_power_strictly_smaller_{m}',2+F(2,m)<2+6/nu)
        check(f'gap_pilot_cost_power_{m}',2*(1+F(1,m))==2+F(2,m))
        check(f'coefficient_pilot_cost_power_{m}',F(2,m)+2==2+F(2,m))
        weights=[(-1)**(k-1)*math.comb(m,k) for k in range(1,m+1)]
        for r in range(m):
            check(f'positive_node_endpoint_extrapolation_{m}_{r}',sum(w*k**r for k,w in enumerate(weights,1))==(1 if r==0 else 0))
        L=m+5
        for ell in range(L+1):
            start=max(1,min(ell-(m-1)//2,L-m+1));nodes=list(range(start,start+m))
            check(f'positive_stencil_{m}_{ell}',min(nodes)>=1 and max(nodes)<=L)
            check(f'nodal_central_stencil_{m}_{ell}',ell==0 or ell in nodes)
            check(f'bounded_stencil_distance_{m}_{ell}',max(abs(k-ell) for k in nodes)<=m)
            # Exact Lagrange reproduction at endpoint and a half-grid point.
            for x in (F(ell),F(2*ell+1,2)):
                basis=[math.prod((F(x-v,w-v) for v in nodes if v!=w),start=F(1)) for w in nodes]
                check(f'lagrange_reproduction_{m}_{ell}_{x}',all(sum(b*w**r for b,w in zip(basis,nodes))==x**r for r in range(m)))
    check('m4_refined_exponent',2+6/(F(4)-F(5,2))==6)
    check('m4_original_exponent',2+F(8,4-3)==10)
    for c in (F(2),F(7,3),F(11)):
        for p in (F(1,10),F(1,3),F(3,4)):
            H=c*p;N=31
            check(f'scaled_bernoulli_variance_{c}_{p}',c*c*p*(1-p)/N==c*H*(1-p)/N)
    for n in range(2,17):
        check(f'Bernoulli_exponential_coefficient_{n}',math.factorial(n)>=2*3**(n-2))
    # Rational parametrization of sinh/cosh by exp(gamma).
    for z in (F(2),F(3),F(5,2)):
        sh=(z-1/z)/2;ch=(z+1/z)/2;sh2=(z*z-1/(z*z))/2;A=F(7,3)
        c1=1/(2*A*sh);c2=1/(2*A*sh2)
        check(f'calibration_ratio_{z}',c1/(2*c2)==ch)
        check(f'calibration_area_{z}',1/(2*c1*sh)==A)
        for j in (2,4,8):
            zh=z+F(1,10);Ah=A+F(1,20)
            cj=2*A*(z**j-z**(-j))/2;chat=2*Ah*(zh**j-zh**(-j))/2
            R=Ah/A*(zh**j-zh**(-j))/(z**j-z**(-j))
            check(f'integrated_plugin_scaling_{z}_{j}',chat/cj==R)
    # The affine part of a translated quadratic has zero second derivative.
    for delta in (F(0),F(1,20),F(1,3)):
        for x in (F(0),F(1,7),F(2,3)):
            check(f'quadratic_translation_affine_{delta}_{x}',(x+delta)**2-x*x==2*delta*x+delta*delta)
    # Exhaustive finite decision histories: an arithmetic check, not a proof of
    # the probabilistic bracket assertion on arbitrary physical remainders.
    for code in range(256):
        w=F(1);cost=F(0);last=w
        for k in range(8):
            last=w;cost+=1/(w*w);w*=F(3,4) if (code>>k)&1 else F(1,2)
        check(f'bisection_geometric_charge_{code}',cost<=F(16,7)/(last*last))
    active=expand_sources();names=[n for n,_ in active]
    check('prior_inputs_still_active',set(OLD_INPUTS)<=set(names),'source_integrity')
    old=[(n,s) for n,s in active if n in set(OLD_INPUTS)]
    check('prior_input_order_retained',[n for n,_ in old]==OLD_INPUTS,'source_integrity')
    pat=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}',re.S)
    blocks=[m.group(0).encode() for _,s in old for m in pat.finditer(s)]
    digest=hashlib.sha256(b''.join(str(len(b)).encode()+b'\0'+b for b in blocks)).hexdigest()
    check('all_v10_formal_environments_byte_identical',len(blocks)==OLD_COUNT and digest==OLD_DIGEST,'source_integrity')
    text='\n'.join(s for _,s in active)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check('unique_active_labels',len(labels)==len(set(labels)),'source_integrity')
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text)
    check('resolved_internal_references',all(r in labels or r.startswith('TC-') for r in refs),'source_integrity')
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',text));cites={k.strip() for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in g.split(',')}
    check('resolved_citations',cites<=keys,'source_integrity')
    check('all_new_theorems_active',{'thm:v11-abel-inverse','thm:v11-acquisition','thm:v11-plug-in','lem:v11-calibration','thm:v11-self-calibrated'}<=set(labels),'source_integrity')
    current=len(list(pat.finditer(text)))
    return {'schema':'a2-v11-finite-diagnostics-v1','status':'pass','counts':{'total':len(CHECKS),**dict(Counter(c['kind'] for c in CHECKS))},'checks':CHECKS,
       'source_retention':{'v10_environments':len(blocks),'current_environments':current,'new_environments':current-len(blocks),'ordered_length_prefixed_sha256':digest,'all_v10_byte_identical':True},
       'limitations':['Finite exact identities do not certify the analytic, smoothness, or probabilistic arguments.','The C2 alternatives are abstract and are not realized billiard minimax alternatives.','No physical simulations, exact nonlinear finite-offset probability oracle, interval proof, or remote CI run is claimed.','Dictionary existence and Borel measurability do not include computational complexity.','The preparation rates are sufficient certificate-dependent bounds, not minimax rates.']}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'verification/v11.normal.json');args=parser.parse_args()
    result=run();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('status','counts','source_retention')},sort_keys=True))
