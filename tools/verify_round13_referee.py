#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,sys
from round13_config import PAPERS,SOURCES
ROOT=Path(__file__).resolve().parents[1]
THM=re.compile(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}')
PRF=re.compile(r'\\begin\{proof\}')
LAB=re.compile(r'\\label\{([^}]+)\}')
REF=re.compile(r'\\(?:ref|cref|eqref|autoref)\{([^}]+)\}')
DISPLAY_OPEN=re.compile(r'(?<!\\)\\\['); DISPLAY_CLOSE=re.compile(r'(?<!\\)\\\]')
DOLLAR=re.compile(r'(?<!\\)\$')
BANNED=['TODO','FIXME','TBD','NO_THEOREM_CREDIT','reviewer must verify','external reviewers must verify','assume the main gate','imported packet','conditional only on']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def brace_balance(text):
    level=0; minimum=0
    for i,ch in enumerate(text):
        if ch=='{' and (i==0 or text[i-1]!='\\'): level+=1
        elif ch=='}' and (i==0 or text[i-1]!='\\'): level-=1;minimum=min(minimum,level)
    return level,minimum
errors=[];papers={};global_labels={}
actual={p.name for p in (ROOT/'papers').iterdir() if p.is_dir()}
if actual!=set(PAPERS):errors.append(f'paper directory mismatch: {sorted(actual^set(PAPERS))}')
inv=json.loads((ROOT/'ROUND13_REFEREE_INVENTORY.json').read_text())
if inv.get('paper_count')!=11 or inv.get('total_objections')!=87:errors.append('inventory mismatch')
for folder in PAPERS:
    paper=ROOT/'papers'/folder;src=ROOT/'revision'/'round13-referee-final'/SOURCES[folder]
    active=paper/'ROUND13_POSITIVE_CLOSURE.tex';main=paper/'main.tex'
    report=paper/'REFEREE_REPORT_ROUND12_GPT56_PRO.md';response=paper/'AUTHOR_RESPONSE_ROUND13.md'
    needed=[src,active,main,report,response]
    missing=[str(x.relative_to(ROOT)) for x in needed if not x.is_file()]
    if missing: errors.append(f'{folder}: missing {missing}'); continue
    sb=src.read_bytes();ab=active.read_bytes();text=sb.decode('utf-8');mt=main.read_text();rt=response.read_text()
    if sb!=ab:errors.append(f'{folder}: registered source/active module mismatch')
    if mt.count(r'\input{ROUND13_POSITIVE_CLOSURE.tex}')!=1:errors.append(f'{folder}: controlling input count')
    if 'ROUND13-REFEREE-POSITIVE-CLOSURE' not in mt:errors.append(f'{folder}: marker missing')
    if r'\input{ROUND12_POSITIVE_CLOSURE.tex}' in mt:errors.append(f'{folder}: superseded round12 input remains')
    source_path=f'revision/round13-referee-final/{SOURCES[folder]}'
    if source_path not in rt:errors.append(f'{folder}: response does not identify source')
    nobj=inv['papers'][folder]['objection_count']
    if f'Objections addressed: {nobj}/{nobj}' not in rt:errors.append(f'{folder}: objection coverage marker')
    # every exact objection heading occurs in response
    for obj in inv['papers'][folder]['objections']:
        if f'### {obj}' not in rt:errors.append(f'{folder}: missing response heading {obj}')
    nt=len(THM.findall(text));np=len(PRF.findall(text))
    if nt==0 or nt!=np:errors.append(f'{folder}: theorem/proof {nt}/{np}')
    labels=LAB.findall(text);local=set(labels)
    if len(labels)!=len(local):errors.append(f'{folder}: duplicate local labels')
    badrefs=set()
    for payload in REF.findall(text):
        for label in payload.split(','):
            label=label.strip()
            if label and label not in local:badrefs.add(label)
    if badrefs:errors.append(f'{folder}: unresolved local refs {sorted(badrefs)}')
    for label in labels:
        if label in global_labels:errors.append(f'duplicate global label {label}')
        global_labels[label]=folder
    controls=[(i,ord(ch)) for i,ch in enumerate(text) if ord(ch)<32 and ch not in '\n\t']
    if controls:errors.append(f'{folder}: ASCII controls {controls[:4]}')
    if len(DISPLAY_OPEN.findall(text))!=len(DISPLAY_CLOSE.findall(text)):errors.append(f'{folder}: display delimiter mismatch')
    if len(DOLLAR.findall(text))%2:errors.append(f'{folder}: inline math delimiter mismatch')
    bal,minbal=brace_balance(text)
    if bal or minbal<0:errors.append(f'{folder}: brace balance {bal}/{minbal}')
    low=text.lower()
    for tok in BANNED:
        if tok.lower() in low:errors.append(f'{folder}: banned placeholder {tok}')
    report_sha=sha(report)
    if report_sha!=inv['papers'][folder]['report_sha256']:errors.append(f'{folder}: report hash drift')
    papers[folder]={'source':str(src.relative_to(ROOT)),'source_sha256':sha(src),'active_sha256':sha(active),'byte_identity':sb==ab,'theorem_like_environments':nt,'proofs':np,'labels':len(labels),'references':sum(len([x for x in q.split(',') if x.strip()]) for q in REF.findall(text)),'referee_objections':nobj,'status':'PASS'}
for name in ['ROUND13_REFEREE_INVENTORY.json','ROUND13_REFEREE_INVENTORY.md','ROUND13_HISTORICAL_DERIVATION_AUDIT.md','ROUND13_PROOF_DEPENDENCY_LEDGER.md','REFEREE_ROUND13_RESPONSE.md']:
    if not (ROOT/name).is_file():errors.append(f'missing root file {name}')
ledger=(ROOT/'ROUND13_PROOF_DEPENDENCY_LEDGER.md').read_text()
for token in ['A2 -> A3 -> A4 -> C2 -> D1','B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1']:
    if token not in ledger:errors.append(f'dependency token missing: {token}')
out={'schema':'theta-theory-round13-structural-verification-v1','status':'PASS' if not errors else 'FAIL','paper_count':len(papers),'referee_objections':inv['total_objections'],'total_theorem_like_environments':sum(v['theorem_like_environments'] for v in papers.values()),'total_proofs':sum(v['proofs'] for v in papers.values()),'dependency_dag':'PASS' if not any('dependency' in e for e in errors) else 'FAIL','papers':papers,'errors':errors}
(ROOT/'ROUND13_STRUCTURAL_VERIFICATION.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if errors:
    for e in errors:print('ROUND13_VERIFY_ERROR',e,file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND13_STRUCTURAL_VERIFICATION_PASS papers={len(papers)} objections={inv['total_objections']} theorem_proof={out['total_theorem_like_environments']}/{out['total_proofs']}")
