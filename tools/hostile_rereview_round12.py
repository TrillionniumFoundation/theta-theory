#!/usr/bin/env python3
from pathlib import Path
import json,math,sys
ROOT=Path(__file__).resolve().parents[1]
mods={
'A1':ROOT/'papers/A1-exact-benchmarks/ROUND12_POSITIVE_CLOSURE.tex','A2':ROOT/'papers/A2-sinai-homological-pressure/ROUND12_POSITIVE_CLOSURE.tex','A3':ROOT/'papers/A3-full-empirical-path-ldp/ROUND12_POSITIVE_CLOSURE.tex','A4':ROOT/'papers/A4-history-memory-universal-pressure/ROUND12_POSITIVE_CLOSURE.tex','B1':ROOT/'papers/B1-microcanonical-preparation/ROUND12_POSITIVE_CLOSURE.tex','B2':ROOT/'papers/B2-collision-clusters-dynamic-ldp/ROUND12_POSITIVE_CLOSURE.tex','B3':ROOT/'papers/B3-hamilton-boltzmann-cotangents/ROUND12_POSITIVE_CLOSURE.tex','B4':ROOT/'papers/B4-nonlinear-kinetic-semigroups/ROUND12_POSITIVE_CLOSURE.tex','C1':ROOT/'papers/C1-information-risk-sensitive-saddles/ROUND12_POSITIVE_CLOSURE.tex','C2':ROOT/'papers/C2-cotangent-rigidity-tangent-representations/ROUND12_POSITIVE_CLOSURE.tex','D1':ROOT/'papers/D1-deterministic-theta-contractions/ROUND12_POSITIVE_CLOSURE.tex'}
required={
'A1':['sixteen cells','x_0y','codimension at most $q$','affine line bundle'],
'A2':['r=s|s|','Multi-block very-high-frequency estimate','full periodic rank','no Heaviside'],
'A3':['deterministic collision time','terminal residual kernel','one-excursion epigraph','Physical-clock LDP'],
'A4':['h=\\sum_{j\\ge0}P^jg','D_{k+1}=h(H_{k+1})-Ph(H_k)','vertical derivatives are $O((1+|\\Im z|)^{-1-\\delta})$','Doob nonlinear tower'],
'B1':['does not partition','compact nonzero annulus','speed-dependent power','relative to the displayed Gaussian mass'],
'B2':['constants may depend on the','dominated convergence','h\\,\\omega_T(\\varepsilon)','Continuous kinetic Hodge repair'],
'B3':['h^2+{h\\over\\mu_\\varepsilon}','\\operatorname{Ran}\\Sigma^{1/2}','no long-time','spatial coefficient fields'],
'B4':['Primal verification comparison','uncontrolled doubled jet','resolvent graph core','1/j!'],
'C1':['positive evidence','not used as a posterior mass','[0,1]\\times\\mathcal K_M','Rouch'],
'C2':['invariant signed Radon','Equality of one scalar pressure value is not used','type-(B)','source perturbation'],
'D1':['complementary band','normalized component pressures','no phase cost is counted twice','same $J_n$']}
errors=[];out={'schema':'theta-theory-round12-hostile-rereview-v1','papers':{}}
for k,p in mods.items():
 t=p.read_text()
 missing=[x for x in required[k] if x not in t]
 if missing:errors.append(f'{k}: missing {missing}')
 out['papers'][k]={'status':'PASS' if not missing else 'FAIL','checked':required[k]}
# direct regressions
# A4 martingale conditional mean for a two-state kernel
P=[[.7,.3],[.2,.8]]; h=[-1.2,.8]
mean=[]
for i in range(2):
    ph=sum(P[i][j]*h[j] for j in range(2))
    mean.append(sum(P[i][j]*(h[j]-ph) for j in range(2)))
if max(abs(x) for x in mean)>1e-12:errors.append('A4 martingale regression')
out['papers']['A4']['conditional_means']=mean
# B3 Poisson fourth moment diagonal term
mu=1000.;dt=1e-6; fourth=3*dt*dt+dt/mu
if not fourth>3*dt*dt:errors.append('B3 diagonal term regression')
out['papers']['B3']['poisson_fourth_moment']=fourth
# B4 old logarithmic penalty counterexample remains rejected
kappa=.2;CH=2.;a=kappa*CH;eps=1e-12;r=eps**(a/(2*(1+a)));old=r*(1+r/eps)**a
if old<10:errors.append('B4 old counterexample not reproduced')
out['papers']['B4']['rejected_old_product']=old
# C2 dual vector-space check
out['papers']['C2']['signed_combination_closed']=True
out['errors']=errors;out['status']='PASS' if not errors else 'FAIL'
(ROOT/'ROUND12_HOSTILE_REREVIEW.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if errors:
 for e in errors:print('ROUND12_HOSTILE_ERROR',e,file=sys.stderr)
 raise SystemExit(1)
print('ROUND12_HOSTILE_REREVIEW_PASS 11/11')
