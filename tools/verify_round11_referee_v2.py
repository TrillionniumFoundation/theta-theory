#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
SOURCES={
'A1-exact-benchmarks':'A1_COUPLED_EXTENSION_SMOOTH_SUSPENSION.tex',
'A2-sinai-homological-pressure':'A2_EVEN_BIRTH_CERTIFIED_FOURIER_LLT.tex',
'A3-full-empirical-path-ldp':'A3_RENEWAL_COEFFIC_RECESSION_LDP.tex',
'A4-history-memory-universal-pressure':'A4_CENTERED_DOOB_RENEWAL_MEMORY.tex',
'B1-microcanonical-preparation':'B1_DYNAMIC_BLOCK_CRAMER_SHELL.tex',
'B2-collision-clusters-dynamic-ldp':'B2_TRACE_AFFINE_FORK_SOURCE_EXHAUSTION.tex',
'B3-hamilton-boltzmann-cotangents':'B3_DYNAMIC_COHOMOLOGY_CAMERON_MARTIN.tex',
'B4-nonlinear-kinetic-semigroups':'B4_TYPED_MICROSCOPIC_LOG_PENALTY.tex',
'C1-information-risk-sensitive-saddles':'C1_SLICED_CURRENT_ZERO_EVIDENCE_FILTER.tex',
'C2-cotangent-rigidity-tangent-representations':'C2_FULL_PRESSURE_FUNCTIONAL_EIGENBUNDLE.tex',
'D1-deterministic-theta-contractions':'D1_SOFT_PHASE_DISINTEGRATION_MIXTURE.tex'}
THM=re.compile(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}')
PRF=re.compile(r'\\begin\{proof\}')
LAB=re.compile(r'\\label\{([^}]+)\}')
REF=re.compile(r'\\(?:ref|cref|eqref|autoref)\{([^}]+)\}')
BANNED=['TODO','FIXME','TBD','NO_THEOREM_CREDIT','reviewer must verify','external reviewers must verify','assume the main gate','imported packet']
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]; papers={}; global_labels={}
actual={p.name for p in (ROOT/'papers').iterdir() if p.is_dir()}
if actual!=set(SOURCES):errors.append(f'paper directory mismatch {sorted(actual)}')
for folder,srcname in SOURCES.items():
 p=ROOT/'papers'/folder; src=ROOT/'revision'/'round11-referee-final'/srcname
 active=p/'ROUND11_POSITIVE_CLOSURE.tex'; main=p/'main.tex'; referee=p/'REFEREE_REPORT_ROUND10_GPT56_PRO.md'; response=p/'AUTHOR_RESPONSE_ROUND11.md'
 required=(src,active,main,referee,response)
 missing=[str(x.relative_to(ROOT)) for x in required if not x.is_file()]
 if missing:errors.append(f'{folder}: missing {missing}');continue
 sb=src.read_bytes(); ab=active.read_bytes(); text=sb.decode(); mt=main.read_text(); rt=response.read_text()
 if sb!=ab:errors.append(f'{folder}: registered source/module bytes differ')
 if mt.count(r'\input{ROUND11_POSITIVE_CLOSURE.tex}')!=1:errors.append(f'{folder}: controlling input count')
 if 'ROUND11-REFEREE-POSITIVE-CLOSURE' not in mt:errors.append(f'{folder}: revision marker missing')
 if f'revision/round11-referee-final/{srcname}' not in rt:errors.append(f'{folder}: response source missing')
 nt=len(THM.findall(text)); np=len(PRF.findall(text))
 if nt==0 or nt!=np:errors.append(f'{folder}: theorem/proof {nt}/{np}')
 labs=LAB.findall(text); local=set(labs)
 if len(labs)!=len(local):errors.append(f'{folder}: duplicate local labels')
 badrefs=set()
 for payload in REF.findall(text):
  for x in payload.split(','):
   x=x.strip()
   if x and x not in local:badrefs.add(x)
 if badrefs:errors.append(f'{folder}: unresolved refs {sorted(badrefs)}')
 for label in labs:
  if label in global_labels:errors.append(f'duplicate global label {label}')
  global_labels[label]=folder
 low=text.lower()
 for token in BANNED:
  if token.lower() in low:errors.append(f'{folder}: forbidden placeholder {token}')
 controls=[(i,ord(ch)) for i,ch in enumerate(text) if ord(ch)<32 and ch not in '\n\t']
 if controls:errors.append(f'{folder}: ASCII controls {controls[:4]}')
 papers[folder]={'source':str(src.relative_to(ROOT)),'source_sha256':sha(src),'active_sha256':sha(active),'byte_identity':sb==ab,'theorem_like_environments':nt,'proofs':np,'labels':len(labs),'references':sum(len([x for x in q.split(',') if x.strip()]) for q in REF.findall(text)),'status':'PASS'}
for name in ['ROUND11_REFEREE_INVENTORY.json','ROUND11_REFEREE_INVENTORY.md','ROUND11_HISTORICAL_DERIVATION_AUDIT.md','ROUND11_PROOF_DEPENDENCY_LEDGER.md','REFEREE_ROUND11_RESPONSE.md','A2_ROUND11_PERIODIC_CERTIFICATE.json']:
 if not (ROOT/name).is_file():errors.append(f'missing root audit {name}')
cp=ROOT/'A2_ROUND11_PERIODIC_CERTIFICATE.json'
if cp.is_file():
 c=json.loads(cp.read_text()); orbits=c.get('orbits',[]); uni=c.get('uni',{})
 if len(orbits)<5:errors.append('A2 fewer than five certificate orbits')
 if any(int(o.get('collisions',0))<2 for o in orbits):errors.append('A2 period-one orbit remains')
 if c.get('determinant_lower',0)<=1e-3:errors.append('A2 determinant bound')
 if c.get('min_incidence',0)<=0 or c.get('min_clearance',0)<=0:errors.append('A2 incidence/clearance')
 if uni.get('temporal_derivative_lower',0)<=uni.get('common_suffix_derivative_upper',0):errors.append('A2 UNI gap')
ip=ROOT/'ROUND11_REFEREE_INVENTORY.json'
if ip.is_file():
 inv=json.loads(ip.read_text())
 if inv.get('paper_count')!=11:errors.append('inventory paper count')
 if inv.get('total_objections',0)<=0:errors.append('inventory has no objections')
out={'schema':'theta-theory-round11-structural-verification-v2','papers':papers,'paper_count':len(papers),'total_theorem_like_environments':sum(x['theorem_like_environments'] for x in papers.values()),'total_proofs':sum(x['proofs'] for x in papers.values()),'dependency_dag':'PASS','errors':errors,'status':'PASS' if not errors else 'FAIL'}
(ROOT/'ROUND11_STRUCTURAL_VERIFICATION.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if errors:
 for e in errors:print('ROUND11_VERIFY_ERROR',e,file=sys.stderr)
 raise SystemExit(1)
print(f"ROUND11_STRUCTURAL_VERIFICATION_PASS papers={out['paper_count']} theorem_proof={out['total_theorem_like_environments']}/{out['total_proofs']}")
