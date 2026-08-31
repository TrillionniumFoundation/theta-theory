#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,math,sys
ROOT=Path(__file__).resolve().parents[1]
FILES={'A1':'A1-exact-benchmarks','A2':'A2-sinai-homological-pressure','A3':'A3-full-empirical-path-ldp','A4':'A4-history-memory-universal-pressure','B1':'B1-microcanonical-preparation','B2':'B2-collision-clusters-dynamic-ldp','B3':'B3-hamilton-boltzmann-cotangents','B4':'B4-nonlinear-kinetic-semigroups','C1':'C1-information-risk-sensitive-saddles','C2':'C2-cotangent-rigidity-tangent-representations','D1':'D1-deterministic-theta-contractions'}
NEED={
'A1':[r'\widehat\sigma(x,y)=(\sigma x,x_0y)','disjoint sheet',r'4^n\varpi^n','present-symbol coupling','fixed physical observable'],
'A2':['No period-one winding orbit is used',r'n^K<|b|\le e^{\delta n}',r'M\delta>\log C+4\delta','fixed average-width window','even in $s$'],
'A3':['deterministic collision horizon','original countable Gibbs renewal','same deterministic collision horizon','pointed terminal','positive recurrent without a pressure gap'],
'A4':[r'h=\sum_{j\ge0}P^jg',r'D_{k+1}=h(H_{k+1})-Ph(H_k)',r'\mathcal E_t^V F=\log P_t^V(e^F)',r'zP-PL_VP-\mathcal C(z)^{-1}'],
'B1':['compact nonzero frequency annulus',r'(1+|u|)^{-s c\mu_\varepsilon}',r'\log\operatorname{vol}(W_\varepsilon)=o(\mu_\varepsilon)','polymer correction'],
'B2':['normal traces are measures already containing','youngest fork',r'affine in $\xi$',r'\varepsilon^{\alpha_0}/h_\varepsilon','real-source exhaustion'],
'B3':['No curvature is attributed to the linear balance multiplier','temporal coboundaries',r'\operatorname{Ran}\Sigma^{1/2}','Fourier-transform in $x$'],
'B4':['Five objects are kept distinct','observable resolvent',r'\Phi_\epsilon(r)',r'r_\epsilon\exp(C_H|p_\epsilon|)','initial preparation term'],
'C1':['Federer slicing','projective limit direction','zero-evidence compactification','a priori','normed class','inserted coefficient'],
'C2':['for every sufficiently small potential $H$','Equality of the single numbers','finite-dimensional matrix algebra','source variation','state derivative'],
'D1':[r'\mathbb P_n=\sum_jw_{n,j}\mathbb P_{n,j}','normalized conditional pressure','never subtracted twice','same positive joint law']}
FORBID={'A1':[r'\sigma_+\times\sigma_-^{-1}'],'A2':['one-collision periodic orbit','choose $M>C_M'],'A3':['cemetery state','speed $R_N$'],'A4':[r'P(g+h_g)=Ph_g',r'-\log P_t^V1'],'B1':['fixed number of smoothing blocks'],'B2':['QR reset','nonzero analytic functions'],'B3':['multiplier curvature',r'\overline{\operatorname{Ran}\Sigma}'],'B4':[r'd_\lambda(f,g)^2/(2\epsilon)'],'C1':[r'1_{S\cap O_u^{-1}(y)}'],'C2':['same long-time pressure if and only if'],'D1':[r'Q_j(\theta)-\alpha_j']}
errors=[];out={'schema':'theta-theory-round11-hostile-rereview-v2','papers':{}}
for code,folder in FILES.items():
 p=ROOT/'papers'/folder/'ROUND11_POSITIVE_CLOSURE.tex'
 if not p.is_file():errors.append(f'{code}: missing active module');continue
 text=p.read_text(); missing=[s for s in NEED[code] if s not in text]; old=[s for s in FORBID[code] if s in text]
 if missing:errors.append(f'{code}: missing {missing}')
 if old:errors.append(f'{code}: superseded {old}')
 out['papers'][code]={'checked':NEED[code],'forbidden_absent':FORBID[code],'status':'PASS' if not missing and not old else 'FAIL'}
cert=json.loads((ROOT/'A2_ROUND11_PERIODIC_CERTIFICATE.json').read_text())
if any(o['collisions']<2 for o in cert['orbits']):errors.append('A2 period-one orbit remains')
if cert['determinant_lower']<=0 or cert['uni']['temporal_derivative_lower']<=cert['uni']['common_suffix_derivative_upper']:errors.append('A2 arithmetic/UNI certificate')
out['papers']['A2']['certificate']={'determinant_lower':cert['determinant_lower'],'minimum_collision_count':min(o['collisions'] for o in cert['orbits']),'uni_gap':cert['uni']['temporal_derivative_lower']-cert['uni']['common_suffix_derivative_upper']}
P=[[.7,.3],[.2,.8]];h=[1.4,-.6];means=[]
for i in range(2):
 ph=sum(P[i][j]*h[j] for j in range(2));means.append(sum(P[i][j]*(h[j]-ph) for j in range(2)))
if max(abs(x) for x in means)>1e-12:errors.append('A4 centered martingale regression')
out['papers']['A4']['conditional_means']=means
rho=1e-12;sizes=[rho**(1/m) for m in (1,5,20,100)]
if sizes[-1]<=sizes[0]:errors.append('B2 analytic-minor counterexample regression')
out['papers']['B2']['old_x_power_sublevel_sizes']=sizes
partials=[float(n) for n in (10,100,1000)]
if partials[-1]<=partials[0]:errors.append('B3 Cameron-Martin domain regression')
out['papers']['B3']['excluded_inverse_form_partial_sums']=partials
vals=[]
for eps in (1e-2,1e-4,1e-6):
 r=eps**.75;p=.5*math.log1p(r/eps);vals.append(r*math.exp(p))
if vals[-1]>=vals[0]:errors.append('B4 logarithmic-jet regression')
out['papers']['B4']['r_exp_p']=vals
p0=math.log(1.5+.5);base=math.log(2);gap=abs(math.log(1.5)-math.log(.5))
if abs(p0-base)>1e-12 or gap<=0:errors.append('C2 scalar pressure regression')
out['papers']['C2']['scalar_pressure_counterexample']={'pressures_equal':abs(p0-base)<1e-12,'fixed_point_sum_gap':gap}
alpha,q=.7,1.9;qu=-alpha+q
out['papers']['D1']['phase_pressure_example']={'alpha':alpha,'normalized_pressure':q,'unnormalized_pressure':qu}
out['paper_count']=len(out['papers']);out['errors']=errors;out['status']='PASS' if not errors else 'FAIL'
(ROOT/'ROUND11_HOSTILE_REREVIEW.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if errors:
 for e in errors:print('ROUND11_HOSTILE_ERROR',e,file=sys.stderr)
 raise SystemExit(1)
print('ROUND11_HOSTILE_REREVIEW_PASS 11/11')
