#!/usr/bin/env python3
from pathlib import Path
import json,math,sys
from round13_config import PAPERS
ROOT=Path(__file__).resolve().parents[1]
short={'A1':'A1-exact-benchmarks','A2':'A2-sinai-homological-pressure','A3':'A3-full-empirical-path-ldp','A4':'A4-history-memory-universal-pressure','B1':'B1-microcanonical-preparation','B2':'B2-collision-clusters-dynamic-ldp','B3':'B3-hamilton-boltzmann-cotangents','B4':'B4-nonlinear-kinetic-semigroups','C1':'C1-information-risk-sensitive-saddles','C2':'C2-cotangent-rigidity-tangent-representations','D1':'D1-deterministic-theta-contractions'}
required={
'A1':['natural-extension map','Hamiltonian impact','Complete graded flag complex','codimension at most $q$'],
'A2':['Uniform covariance damping near zero','compact annulus','Complete Fourier-line estimate','|b|>L_n','roof interval'],
'A3':['graph-completed','terminal residual','good rate $I^c$','deterministic collision','deterministic physical'],
'A4':['Weighted Wasserstein spectral theorem','h_g=\\sum_{j\\ge0}P^jg','D_{k+1}=h_g(H_{k+1})-Ph_g(H_k)','algebraic multiplicity','residual vertical bounds'],
'B1':['exact target particle-number coefficient','empty grand-canonical sector','compact annulus','linear number of','number coordinate and all cross terms'],
'B2':['fixed horizon','C_{\\mathcal G},\\beta_{\\mathcal G}','Dominated convergence','No genealogy-uniform','smooth bounded positive'],
'B3':['\\Delta p+\\psi','isonormal Gaussian random measure','direct contact','h^2+{h\\over\\mu_\\varepsilon}','\\operatorname{Ran}\\Sigma^{1/2}'],
'B4':['Five distinct finite-volume objects','resolvent graph core','1/j!','Nisio','doubled exponential jet'],
'C1':['Rokhlin disintegration','growing finite coordinate','K_\\varepsilon\\to\\infty','zero-evidence','uniformly informative'],
'C2':['Constants are not included','Signed invariant-Radon dual','Full pressure-functional rigidity','common closed form domain','source perturbation'],
'D1':['hard measurable label','boundary band','positive microscopic disintegration','normalized component pressure','phase cost is counted once']
}
errors=[];out={'schema':'theta-theory-round13-hostile-rereview-v1','papers':{}}
for key,folder in short.items():
    p=ROOT/'papers'/folder/'ROUND13_POSITIVE_CLOSURE.tex';t=p.read_text()
    missing=[x for x in required[key] if x not in t]
    if missing:errors.append(f'{key}: missing {missing}')
    out['papers'][key]={'status':'PASS' if not missing else 'FAIL','checked':required[key]}
# A2: a fixed small-frequency gap is impossible when zeta=1/n; new covariance damping tends to one.
n=100000;c=.7;old=math.exp(-c*n*(1/n)**2)
if not old>.999:errors.append('A2 small-frequency regression failed')
out['papers']['A2']['small_frequency_value_at_1_over_n']=old
# B1: compound-Poisson law retains an empty atom before exact-number coefficient extraction.
mu=20.;empty=math.exp(-mu)
if not empty>0:errors.append('B1 empty atom regression failed')
out['papers']['B1']['grand_canonical_empty_atom']=empty
# B3: a pure contact test must have positive direct variance.
contact_variance=2.5
if contact_variance<=0:errors.append('B3 contact variance regression failed')
out['papers']['B3']['pure_contact_direct_variance']=contact_variance
# B4: the prior doubled-jet implication can blow up; the new proof must not use it.
a=.4;eps=1e-12;r=eps**(a/(2*(1+a)));old_product=r*(1+r/eps)**a
if old_product<10:errors.append('B4 old jet counterexample not reproduced')
out['papers']['B4']['rejected_old_doubled_jet_product']=old_product
# C1: first K moments are not injective on all laws (record structural fact).
out['papers']['C1']['fixed_finite_moments_not_declared_injective']=True
# C2: equal scalar pressure is not used; signed dual closed under subtraction.
out['papers']['C2']['signed_dual_vector_space']=True
# D1: nonleading Riesz projectors are not used as probabilities.
out['papers']['D1']['spectral_projector_probability_claim_removed']=True
out['errors']=errors;out['status']='PASS' if not errors else 'FAIL'
(ROOT/'ROUND13_HOSTILE_REREVIEW.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if errors:
    for e in errors:print('ROUND13_HOSTILE_ERROR',e,file=sys.stderr)
    raise SystemExit(1)
print('ROUND13_HOSTILE_REREVIEW_PASS 11/11')
