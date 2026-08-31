#!/usr/bin/env python3
"""Fail-closed structural/source verifier for Round Ten."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'revision'/'round10-referee-final'
MANIFEST=ROOT/'ROUND10_MATERIALIZATION_MANIFEST.json'
EXPECTED={
'A1-exact-benchmarks':'A1_MAPPING_TORUS_ONE_SIDED_RESPONSE.tex',
'A2-sinai-homological-pressure':'A2_EXPLICIT_CERTIFICATE_FOURIER_RANGES.tex',
'A3-full-empirical-path-ldp':'A3_DETERMINISTIC_SPEED_PROJECTIVE_FLOW_LDP.tex',
'A4-history-memory-universal-pressure':'A4_DOOB_PAST_KERNEL_MEMORY.tex',
'B1-microcanonical-preparation':'B1_INTERIOR_SADDLE_REGENERATIVE_SHELL.tex',
'B2-collision-clusters-dynamic-ldp':'B2_COMPATIBLE_TRACE_INTEGRATED_JACOBI_LDP.tex',
'B3-hamilton-boltzmann-cotangents':'B3_COVARIANCE_FIRST_GAUGE_PROCESS.tex',
'B4-nonlinear-kinetic-semigroups':'B4_DYNAMIC_ACTION_GRAPH_CORE_COMPARISON.tex',
'C1-information-risk-sensitive-saddles':'C1_STRATIFIED_EVIDENCE_FILTERING.tex',
'C2-cotangent-rigidity-tangent-representations':'C2_COMMON_TRANSFER_BUNDLE_COTANGENTS.tex',
'D1-deterministic-theta-contractions':'D1_MICROSCOPIC_PHASE_DISINTEGRATION.tex',
}
REQUIRED={
'A1-exact-benchmarks':['Physical--symbolic factor without a Cantor section','Exact autonomous Hamiltonian suspension','Correct one-sided Lasota--Yorke estimate','Bounded material current insertions'],
'A2-sinai-homological-pressure':['Renormalized one-sided birth bundle','Verified four-coordinate periodic certificate','Verified returned-branch UNI','Four-range twisted estimate','Uniform density LLT'],
'A3-full-empirical-path-ldp':['The speed is the deterministic integer','State sufficiency and exponential tightness','Projective marked-flow LDP','Actual recession principle','deterministic horizon'],
'A4-history-memory-universal-pressure':['past sigma-field','Conditional martingale--coboundary decomposition','Eigenfunction-normalized nonlinear semigroup','zP-PL_\\Psi P-C(z)^{-1}'],
'B1-microcanonical-preparation':['relative interior','Typical-sector covariance','Good-block minorization','Full mixed lattice--continuous characteristic estimate','Uniform exact-saddle shell coefficient'],
'B2-collision-clusters-dynamic-ldp':['Closed Green graph and reflected transport','Flux-weighted Jacobi small-ball estimate','Integrated first-surplus gain','Scaled one-block theorem','Exact conservative regularization'],
'B3-hamilton-boltzmann-cotangents':['raw second variation may be indefinite','Linearized biased Boltzmann well-posedness','Projective Gaussian covariance','Second epi-derivative and covariance inverse','Localized connected-cumulant estimate'],
'B4-nonlinear-kinetic-semigroups':['Five objects are kept distinct','Observable resolvent core','Full-hierarchy terminal corrector','dynamic cost','Coercive diagonal comparison'],
'C1-information-risk-sensitive-saddles':['unnormalized observation current','Evidence lift','Feller evidence kernel','Uniform coarea local coefficient','reachable cluster'],
'C2-cotangent-rigidity-tangent-representations':['closed linear nullspaces','uniform Ces','Kato transport without infinite-path Radon--Nikodym densities','Covariant compressed resolvent','Typed nonlinear contraction'],
'D1-deterministic-theta-contractions':['disjoint measurable phase basins','Microscopic phase mixture LDP','Lee--Yang','Labelled projective LDP','Exact labelled and unlabelled shell conditioning'],
}
THEOREM=re.compile(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}')
PROOF=re.compile(r'\\begin\{proof\}')
LABEL=re.compile(r'\\label\{([^}]+)\}')
REF=re.compile(r'\\(?:ref|cref)\{([^}]+)\}')
BANNED=['TODO','FIXME','TBD','NO_THEOREM_CREDIT','reviewer must verify','external reviewers must verify','assume the main gate','imported analytic packet','conditional on the principal theorem']

errors=[]
report={'schema':'theta-theory-round10-structural-verification-v1','papers':{},'dependency_dag':'PASS'}
if not MANIFEST.is_file(): errors.append('materialization manifest missing')
else:
    man=json.loads(MANIFEST.read_text())
    if man.get('status')!='PASS' or man.get('paper_count')!=11: errors.append('materialization manifest is not PASS 11/11')

all_labels={}
total_theorems=total_proofs=0
for folder,source_name in EXPECTED.items():
    paper=ROOT/'papers'/folder
    source=SRC/source_name
    active=paper/'ROUND10_POSITIVE_CLOSURE.tex'
    main=paper/'main.tex'
    response=paper/'AUTHOR_RESPONSE_ROUND10.md'
    for q in (source,active,main,response):
        if not q.is_file(): errors.append(f'{folder}: missing {q.relative_to(ROOT)}')
    if not all(q.is_file() for q in (source,active,main,response)): continue
    if source.read_bytes()!=active.read_bytes(): errors.append(f'{folder}: registered/active byte mismatch')
    text=active.read_text(encoding='utf-8')
    main_text=main.read_text(encoding='utf-8')
    controls=[(i,b) for i,b in enumerate(active.read_bytes()) if b<32 and b not in (9,10,13)]
    if controls: errors.append(f'{folder}: ASCII controls {controls[:8]}')
    th=len(THEOREM.findall(text)); pr=len(PROOF.findall(text))
    total_theorems+=th; total_proofs+=pr
    if th==0 or th!=pr: errors.append(f'{folder}: theorem/proof mismatch {th}/{pr}')
    labels=LABEL.findall(text)
    if len(labels)!=len(set(labels)): errors.append(f'{folder}: duplicate local labels')
    for lab in labels:
        if lab in all_labels: errors.append(f'global duplicate label {lab}: {all_labels[lab]}, {folder}')
        all_labels[lab]=folder
    refs=[]
    for payload in REF.findall(text): refs.extend(x.strip() for x in payload.split(',') if x.strip())
    missing=sorted(set(refs)-set(labels))
    if missing: errors.append(f'{folder}: unresolved local refs {missing}')
    if main_text.count(r'\input{ROUND10_POSITIVE_CLOSURE.tex}')!=1: errors.append(f'{folder}: controlling input count')
    if 'ROUND10-REFEREE-POSITIVE-CLOSURE' not in main_text: errors.append(f'{folder}: controlling marker missing')
    if r'\input{ROUND9_POSITIVE_CLOSURE.tex}' in main_text: errors.append(f'{folder}: obsolete round-nine input active')
    low=text.lower()
    for token in BANNED:
        if token.lower() in low: errors.append(f'{folder}: forbidden placeholder {token}')
    for snippet in REQUIRED[folder]:
        if snippet not in text: errors.append(f'{folder}: required gate missing: {snippet}')
    report['papers'][folder]={
       'source':f'revision/round10-referee-final/{source_name}',
       'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
       'active_sha256':hashlib.sha256(active.read_bytes()).hexdigest(),
       'byte_identity':source.read_bytes()==active.read_bytes(),
       'theorem_like_environments':th,'proofs':pr,'labels':len(labels),'references':len(refs),'status':'PASS'
    }

# Acyclic declared dependency graph.
graph={
 'A1':[], 'A2':[], 'A3':['A2'], 'A4':['A2','A3'],
 'B2-GC':[], 'B1':['B2-GC'], 'B2-MC':['B1','B2-GC'],
 'B3':['B1','B2-MC'], 'B4':['B1','B2-MC','B3'],
 'C1':['B4'], 'C2':['A4','B3','B4'], 'D1':['A3','A4','B2-MC','B4','C1','C2'],
}
seen=set(); temp=set()
def visit(n):
    if n in temp: raise RuntimeError(f'cycle at {n}')
    if n in seen: return
    temp.add(n)
    for d in graph[n]: visit(d)
    temp.remove(n); seen.add(n)
try:
    for n in graph: visit(n)
except Exception as e:
    errors.append(str(e)); report['dependency_dag']='FAIL'

# Model-specific executable certificate.
try:
    cp=subprocess.run([sys.executable,str(ROOT/'tools'/'verify_a2_round10_certificate.py')],cwd=ROOT,capture_output=True,text=True,check=True)
    report['a2_certificate']=cp.stdout.strip()
except subprocess.CalledProcessError as e:
    errors.append('A2 certificate failed: '+e.stdout+e.stderr)

for required_root in ['ROUND10_HISTORICAL_DERIVATION_AUDIT.md','ROUND10_PROOF_DEPENDENCY_LEDGER.md','ROUND10_REFEREE_INVENTORY.md','ROUND10_REFEREE_INVENTORY.json','REFEREE_ROUND10_RESPONSE.md','ROUND10_INTERNAL_HARSH_REREVIEW.md']:
    if not (ROOT/required_root).is_file(): errors.append(f'missing root record {required_root}')

report['paper_count']=len(EXPECTED)
report['total_theorem_like_environments']=total_theorems
report['total_proofs']=total_proofs
report['errors']=errors
report['status']='PASS' if not errors else 'FAIL'
(ROOT/'ROUND10_STRUCTURAL_VERIFICATION.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
if errors:
    for e in errors: print('ROUND10_VERIFY_ERROR',e,file=sys.stderr)
    raise SystemExit(1)
print(f'ROUND10_STRUCTURAL_VERIFICATION_PASS papers=11 theorem_proof={total_theorems}/{total_proofs}')
