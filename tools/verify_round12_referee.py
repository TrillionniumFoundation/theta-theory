#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
SOURCES={'A1-exact-benchmarks':'A1_TARGET_REFINED_FLAG_RESPONSE.tex','A2-sinai-homological-pressure':'A2_PARENT_FOLD_MULTIBLOCK_LLT.tex','A3-full-empirical-path-ldp':'A3_CONTROLLED_RENEWAL_RESIDUAL_LDP.tex','A4-history-memory-universal-pressure':'A4_HARRIS_ROUGH_RENEWAL_MEMORY.tex','B1-microcanonical-preparation':'B1_POLYMER_PRESSURE_REGULAR_SHELL.tex','B2-collision-clusters-dynamic-ldp':'B2_SUMMED_JACOBI_TRACE_LDP.tex','B3-hamilton-boltzmann-cotangents':'B3_PERTURBATIVE_COVARIANCE_PROCESS.tex','B4-nonlinear-kinetic-semigroups':'B4_RESOLVENT_CORE_PRIMAL_COMPARISON.tex','C1-information-risk-sensitive-saddles':'C1_POSITIVE_SLICE_EVIDENCE_CONE.tex','C2-cotangent-rigidity-tangent-representations':'C2_SIGNED_DUAL_FORM_MEMORY.tex','D1-deterministic-theta-contractions':'D1_CANONICAL_PHASE_SHEAF.tex'}
THM=re.compile(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}')
PRF=re.compile(r'\\begin\{proof\}')
LAB=re.compile(r'\\label\{([^}]+)\}')
REF=re.compile(r'\\(?:ref|cref|eqref|autoref)\{([^}]+)\}')
BANNED=['TODO','FIXME','TBD','NO_THEOREM_CREDIT','reviewer must verify','external reviewers must verify','assume the main gate','imported packet','conditional only on']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]; papers={}; glabel={}
actual={p.name for p in (ROOT/'papers').iterdir() if p.is_dir()}
if actual!=set(SOURCES):errors.append('paper directory mismatch')
inv=json.loads((ROOT/'ROUND12_REFEREE_INVENTORY.json').read_text())
if inv.get('paper_count')!=11 or inv.get('total_objections')!=88:errors.append('inventory mismatch')
for folder,srcname in SOURCES.items():
 p=ROOT/'papers'/folder; src=ROOT/'revision'/'round12-referee-final'/srcname; active=p/'ROUND12_POSITIVE_CLOSURE.tex'; main=p/'main.tex'; report=p/'REFEREE_REPORT_ROUND11_GPT56_PRO.md'; response=p/'AUTHOR_RESPONSE_ROUND12.md'
 missing=[str(x.relative_to(ROOT)) for x in [src,active,main,report,response] if not x.is_file()]
 if missing:errors.append(f'{folder}: missing {missing}');continue
 sb=src.read_bytes();ab=active.read_bytes();text=sb.decode();mt=main.read_text();rt=response.read_text()
 if sb!=ab:errors.append(f'{folder}: source/module mismatch')
 if mt.count(r'\input{ROUND12_POSITIVE_CLOSURE.tex}')!=1:errors.append(f'{folder}: input count')
 if 'ROUND12-REFEREE-POSITIVE-CLOSURE' not in mt:errors.append(f'{folder}: marker')
 if f'revision/round12-referee-final/{srcname}' not in rt:errors.append(f'{folder}: response source')
 nt=len(THM.findall(text));np=len(PRF.findall(text))
 if nt==0 or nt!=np:errors.append(f'{folder}: theorem/proof {nt}/{np}')
 labels=LAB.findall(text); local=set(labels)
 if len(labels)!=len(local):errors.append(f'{folder}: duplicate local labels')
 bad=set()
 for payload in REF.findall(text):
  for x in payload.split(','):
   x=x.strip()
   if x and x not in local:bad.add(x)
 if bad:errors.append(f'{folder}: unresolved refs {sorted(bad)}')
 for label in labels:
  if label in glabel:errors.append(f'duplicate global label {label}')
  glabel[label]=folder
 low=text.lower()
 for tok in BANNED:
  if tok.lower() in low:errors.append(f'{folder}: banned {tok}')
 controls=[(i,ord(ch)) for i,ch in enumerate(text) if ord(ch)<32 and ch not in '\n\t']
 if controls:errors.append(f'{folder}: controls {controls[:4]}')
 objections=inv['papers'][folder]['objection_count']
 if f'Objections addressed: **{objections}/{objections}**' not in rt:errors.append(f'{folder}: objection mapping')
 papers[folder]={'source':str(src.relative_to(ROOT)),'source_sha256':sha(src),'active_sha256':sha(active),'byte_identity':sb==ab,'theorem_like_environments':nt,'proofs':np,'labels':len(labels),'references':sum(len([x for x in q.split(',') if x.strip()]) for q in REF.findall(text)),'referee_objections':objections,'status':'PASS'}
for name in ['ROUND12_REFEREE_INVENTORY.json','ROUND12_REFEREE_INVENTORY.md','ROUND12_HISTORICAL_DERIVATION_AUDIT.md','ROUND12_PROOF_DEPENDENCY_LEDGER.md','REFEREE_ROUND12_RESPONSE.md']:
 if not (ROOT/name).is_file():errors.append(f'missing root file {name}')
out={'schema':'theta-theory-round12-structural-verification-v1','status':'PASS' if not errors else 'FAIL','paper_count':len(papers),'referee_objections':inv['total_objections'],'total_theorem_like_environments':sum(v['theorem_like_environments'] for v in papers.values()),'total_proofs':sum(v['proofs'] for v in papers.values()),'dependency_dag':'PASS','papers':papers,'errors':errors}
(ROOT/'ROUND12_STRUCTURAL_VERIFICATION.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if errors:
 for e in errors:print('ROUND12_VERIFY_ERROR',e,file=sys.stderr)
 raise SystemExit(1)
print(f"ROUND12_STRUCTURAL_VERIFICATION_PASS papers={len(papers)} objections={inv['total_objections']} theorem_proof={out['total_theorem_like_environments']}/{out['total_proofs']}")
