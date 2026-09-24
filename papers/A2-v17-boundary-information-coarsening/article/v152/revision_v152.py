#!/usr/bin/env python3
"""Pinned, non-destructive assembly and native verification for A2 v152."""
from pathlib import Path
from collections import Counter
import hashlib,json,os,re,shutil,subprocess,sys,platform
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'v151';ROOT=HERE.parents[3]
PREFIX='papers/A2-v17-boundary-information-coarsening/article/v152'
BRANCH='revision/a2-v152-divisor-conductor-collision-geometry-2026-09-24'
REVIEW='11c9e91135c5e8bb3ee61a067d76286d81a3df7d'
REPORT='reviews/a2-v151-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md'
REPORT_BLOB='2d6737c4de6a774e1a607a1eecc09316901cc4ed'
GENERATED={'SOURCE_LOCK_V152.json','NONDELETION_V152.json','PROVENANCE_MANIFEST_V152.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
def dump(p,x):put(p,json.dumps(x,indent=2)+'\n')
def source(p,r):return p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and not any(k in r.parts for k in ('evidence','evidence_v152','__pycache__'))
def expand(p,root):return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(root/(m[1] if m[1].endswith('.tex') else m[1]+'.tex'),root),p.read_text())
def entry(commit=None):
    state=f'Verified native publication from source commit `{commit}`.' if commit else 'Mathematical source staged; completed verification is asserted only by the v152 build receipt.'
    put(ROOT/'CURRENT_REVIEW_ENTRY.md',f'''# A2 referee entry — revision 152

{state}

Branch: `{BRANCH}`. Controlling review: `{REVIEW}`.

**Principal article:** [geometry.pdf]({PREFIX}/geometry.pdf) · [LaTeX]({PREFIX}/geometry.tex).

[Response to v151]({PREFIX}/RESPONSE_TO_V151_REPORT.md) · [Reading guide]({PREFIX}/README.md) · [Issue matrix]({PREFIX}/ISSUE_MATRIX_V152.json).

New mathematics: conductor and singular-scheme formulas for split divisor branches; exact binary collision model and Cohen–Macaulay criterion; reduced intersections of divisor-degree images; a universal genuinely ramified point in every pencil failure-algebra orbit closure; full reciprocal-polynomial normalization-fibre equations. All v151 principal mathematical blocks and parts are retained.

[Build receipt]({PREFIX}/evidence_v152/BUILD_RECEIPT_V152.json) · [Theorem locator]({PREFIX}/evidence_v152/THEOREM_LOCATOR_V152.json) · [Source lock]({PREFIX}/SOURCE_LOCK_V152.json) · [Preservation]({PREFIX}/NONDELETION_V152.json) · [Primary-source audit]({PREFIX}/LITERATURE_AUDIT_V152.md).

[Applications]({PREFIX}/applications.pdf) remain separate; [archive-v144.pdf]({PREFIX}/archive-v144.pdf) is non-submitted history. The full Ballico 1993 theorem/proof text remains documentary-open. Finite checks do not certify universal proofs, historical priority, or journal acceptance.
''')
def assemble():
    if not BASE.is_dir():raise RuntimeError('Pinned v151 baseline missing')
    hist=HERE/'history/v151-root';hist.mkdir(parents=True,exist_ok=True);records={}
    for p in BASE.rglob('*'):
        r=p.relative_to(BASE)
        if not source(p,r):continue
        dest=hist/p.name if len(r.parts)==1 else HERE/r
        if dest.exists() and sha(dest)!=sha(p):raise RuntimeError('Inherited source changed: '+str(r))
        if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        active=HERE/r
        if not active.exists():active.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,active)
        records[str(r)]={'sha256':sha(p),'preserved_at':str(dest.relative_to(HERE))}
    dump(HERE/'INHERITED_SOURCE_V152.json',{'predecessor_review_commit':REVIEW,'files':records})
    report=ROOT/REPORT
    if report.exists():
        b=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if blob!=REPORT_BLOB:raise RuntimeError('Controlling report blob mismatch')
        target=HERE/'review_inputs/v151_REFEREE_REPORT.md';target.parent.mkdir(exist_ok=True);shutil.copy2(report,target)
    elif os.environ.get('GITHUB_ACTIONS'):raise RuntimeError('Controlling review missing')
    entry();print('Preserved',len(records),'predecessor source files',flush=True)
def build():
    os.chdir(HERE);ev=HERE/'evidence_v152';ev.mkdir(exist_ok=True);(HERE/'evidence').mkdir(exist_ok=True)
    names='exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact revision137_exact revision138_exact revision139_exact revision140_exact revision141_spectral_exact revision141_likelihood_exact revision142_exact revision143_critical_exact revision144_projective_exact'.split()
    scripts=['checks/'+n+'.py' for n in names]+['check_v145.py','check_v146.py','check_local_v146.py','check_v147.py','check_v148.py','check_v149.py','check_v151.py','check_v152.py'];records=[]
    for script in scripts:
        print('Executing',script,flush=True);log=ev/(Path(script).stem+'.log')
        with log.open('w') as f:r=subprocess.run([sys.executable,script],stdout=f,stderr=subprocess.STDOUT)
        records.append({'script':script,'sha256':sha(HERE/script),'returncode':r.returncode,'log':str(log.relative_to(HERE))})
        dump(ev/'EXECUTED_CHECKS_V152.json',records)
        if r.returncode:print(log.read_text()[-10000:]);raise RuntimeError('Regression failed: '+script)
    for name in ('geometry','applications','archive-v144'):
        for ext in ('aux','out','toc'):(HERE/(name+'.'+ext)).unlink(missing_ok=True)
        for k in range(1,4):
            print('Native LaTeX',name,k,flush=True)
            with (ev/(name+'-pass'+str(k)+'.log')).open('w') as f:r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],stdout=f,stderr=subprocess.STDOUT)
            if r.returncode:print((ev/(name+'-pass'+str(k)+'.log')).read_text()[-10000:]);raise RuntimeError('Build failed: '+name)
        aux=(HERE/(name+'.aux')).read_text()
        put(HERE/(name+'-labels.aux'),'\n'.join(l for l in aux.splitlines() if l.startswith('\\newlabel{') and not l.startswith('\\newlabel{tocindent'))+'\n')
        shutil.copy2(HERE/(name+'.log'),ev/(name+'-final.log'))
    verify()
def verify():
    ev=HERE/'evidence_v152';texts={n:expand(HERE/(n+'.tex'),HERE) for n in ('geometry','applications','archive-v144')}
    labels=lambda t:re.findall(r'\\label\{([^}]+)\}',t)
    refs=lambda t:set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',t))
    main=texts['geometry'];old=expand(BASE/'geometry.tex',BASE);checks={}
    checks['principal_references_self_contained']=not(refs(main)-set(labels(main))) and '\\externaldocument' not in main
    checks['applications_references_resolve']=not(refs(texts['applications'])-set(labels(main))-set(labels(texts['applications'])))
    checks['archive_references_resolve']=not(refs(texts['archive-v144'])-set(labels(texts['archive-v144'])))
    pdfs={}
    for n,t in texts.items():
        log=(ev/(n+'-final.log')).read_text(errors='replace')
        checks[n+'_unique_labels']=len(labels(t))==len(set(labels(t)))
        checks[n+'_resolved_references']=not bool(re.search(r'(There were undefined references|Citation .+ undefined|Reference .+ undefined|multiply defined|Rerun to get cross-references)',log))
        checks[n+'_no_overfull_boxes']=not bool(re.search(r'Overfull \\[hv]box',log))
        p=HERE/(n+'.pdf');info=subprocess.check_output(['pdfinfo',str(p)],text=True)
        pdfs[n]={'pages':int(re.search(r'^Pages:\s*(\d+)',info,re.M)[1]),'bytes':p.stat().st_size,'sha256':sha(p)}
    rec=json.loads((ev/'EXECUTED_CHECKS_V152.json').read_text())
    checks['all_28_scripts_pass']=len(rec)==28 and all(r['returncode']==0 and sha(HERE/r['script'])==r['sha256'] for r in rec)
    exact=json.loads((ev/'REVISION152_EXACT.json').read_text());checks['42_new_exact_checks_pass']=exact['ok'] and exact['check_count']==42
    inherited=json.loads((HERE/'INHERITED_SOURCE_V152.json').read_text())['files']
    checks['every_v151_source_preserved']=all((HERE/r['preserved_at']).is_file() and sha(HERE/r['preserved_at'])==r['sha256'] for r in inherited.values())
    checks['all_v151_parts_unchanged']=all(sha(HERE/p.relative_to(BASE))==sha(p) for p in (BASE/'parts').rglob('*.tex'))
    pattern=r'\\begin\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}[\s\S]*?\\end\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}'
    oldblocks=re.findall(pattern,old);newblocks=re.findall(pattern,main)
    checks['all_v151_principal_math_blocks_retained']=not(Counter(oldblocks)-Counter(newblocks))
    checks['all_v151_principal_labels_retained']=set(labels(old))<=set(labels(main))
    for name in ('applications','archive-v144'):checks[name+'_driver_unchanged']=sha(HERE/(name+'.tex'))==sha(BASE/(name+'.tex'))
    required={'thm:split-conductor-v152','thm:binary-pinch-v152','cor:collision-strata-v152','prop:degree-intersections-v152','thm:universal-boundary-v152','lem:flag-jets-v152','prop:pure-power-fibre-v152','ex:n3-boundary-v152'}
    checks['new_results_in_principal_article']=required<=set(labels(main))
    abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',main)[1]
    checks['abstract_at_most_200_words']=len(abstract.split())<=200
    checks['specific_AI_idea_disclosure']='GPT-6 Astra Pro assisted specifically' in main
    checks['stratum_in_abstract']='maximal-lower-Hilbert-function' in abstract
    commit=os.environ.get('A2_SOURCE_COMMIT','LOCAL-PREFLIGHT-NOT-REMOTE')
    receipt={'revision':152,'source_commit':commit,'controlling_review_commit':REVIEW,'controlling_review_blob':REPORT_BLOB,'all_checks_pass':all(checks.values()),'checks':checks,'executed_script_count':len(rec),'new_exact_check_count':exact['check_count'],'executed_scripts':rec,'pdfs':pdfs,'labels':{n:len(labels(t)) for n,t in texts.items()},'preserved_predecessor_source_files':len(inherited),'preserved_principal_math_blocks':len(oldblocks),'proof_certified_by_computation':False,'Ballico_1993_full_text_comparison_completed':False,'historical_priority_certified':False,'journal_acceptance_asserted':False}
    locator={lab:{'number':num,'page':page} for lab,num,page in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{([^}]+)\}',(HERE/'geometry.aux').read_text()) if lab in required}
    dump(ev/'THEOREM_LOCATOR_V152.json',locator);dump(ev/'BUILD_RECEIPT_V152.json',receipt)
    dump(HERE/'NONDELETION_V152.json',{'source_commit':commit,'predecessor_review_commit':REVIEW,'all_source_bytes_preserved':checks['every_v151_source_preserved'],'all_principal_math_blocks_retained':checks['all_v151_principal_math_blocks_retained'],'all_v151_parts_unchanged':checks['all_v151_parts_unchanged'],'source_files':inherited,'preservation_is_not_proof_certification':True})
    dump(HERE/'PROVENANCE_MANIFEST_V152.json',{'source_commit':commit,'sha256':{str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if source(p,p.relative_to(HERE)) and p.name not in GENERATED}})
    dump(HERE/'SOURCE_LOCK_V152.json',{'revision':152,'source_commit':commit,'controlling_review_commit':REVIEW,'principal_manuscript':'geometry.pdf','separate_application':'applications.pdf','non_submitted_archive':'archive-v144.pdf','receipt':'evidence_v152/BUILD_RECEIPT_V152.json','all_checks_pass':receipt['all_checks_pass'],'historical_priority_certified':False})
    import sympy,numpy
    dump(ev/'BUILD_ENVIRONMENT_V152.json',{'source_commit':commit,'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'python':sys.version,'platform':platform.platform(),'sympy':sympy.__version__,'numpy':numpy.__version__,'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[:2]})
    print(json.dumps(receipt,indent=2),flush=True)
    if not receipt['all_checks_pass']:raise RuntimeError('v152 audit failed')
    entry(commit)
if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in {'assemble','build','verify'}:raise SystemExit('Usage: revision_v152.py assemble|build|verify')
    globals()[sys.argv[1]]()
