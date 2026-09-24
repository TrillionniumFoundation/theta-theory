#!/usr/bin/env python3
"""Build the isolated A2 v147 paper and source-bound evidence.

assemble overlays v147 additions onto the immutable v146 tree. build executes
all 24 regressions and native LaTeX builds; it does not certify the proofs.
Only v147 and the A2 CURRENT_REVIEW_ENTRY.md may be written by this helper.
"""
from pathlib import Path
from collections import Counter
import hashlib, json, os, re, shutil, subprocess, sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'v146'
ROOT=HERE.parents[3]
PREFIX='papers/A2-v17-boundary-information-coarsening/article/v147'
REVIEW='855c73b3a0381bebd8d5e0d382fa06125904a73f'
BRANCH='revision/a2-v147-intrinsic-family-descent-2026-09-24'
GENERATED={'SOURCE_LOCK_V147.json','NONDELETION_V147.json','PROVENANCE_MANIFEST_V147.json'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,text):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text)
def dump(p,data): put(p,json.dumps(data,indent=2)+'\n')
def expand(p,root):
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(root/(m[1] if m[1].endswith('.tex') else m[1]+'.tex'),root),p.read_text())
def is_source(p,rel):
    return p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and not any(x in rel.parts for x in ('evidence','__pycache__'))

def entry(source=None):
    lead=('Verified native build from source commit `'+source+'`. The source-bound receipt records 24 completed regressions, three native PDFs, preservation and layout checks. These do not certify mathematical correctness or priority.' if source else
          'A2 v147 source entry. Consult the source-bound receipt for completed build evidence; this source entry alone does not imply a successful build.')
    put(ROOT/'CURRENT_REVIEW_ENTRY.md',f'''# A2 referee entry — revision 147

{lead}

Controlling report: `{REVIEW}` on `review/a2-v146-independent-harsh-top4-2026-09-24`.
Revision branch: `{BRANCH}`.

**Principal manuscript:** [geometry.pdf]({PREFIX}/geometry.pdf) · [LaTeX]({PREFIX}/geometry.tex).

[Point-by-point response]({PREFIX}/RESPONSE_TO_V146_REPORT.md) · [Reading guide]({PREFIX}/README.md) · [Issue matrix]({PREFIX}/ISSUE_MATRIX_V147.json).

[Source lock]({PREFIX}/SOURCE_LOCK_V147.json) · [Build receipt]({PREFIX}/evidence/BUILD_RECEIPT_V147.json) · [Source preservation]({PREFIX}/NONDELETION_V147.json) · [Literature audit]({PREFIX}/LITERATURE_AUDIT_V147.md).

The principal addition is a general unmarked inverse for moving Schur coefficient subspaces, including actual bundle descent. Two isotrivial rank-712 thickenings with the same Artin fibres and the same graded vector bundles are separated by this inverse. The first-relation orbit proposition, represented local automorphism sequence and inverse-system comparison isolate the geometric contribution. All previous all-pencil, local, curve, moving, sharpness and spectral results are retained.

[Separate applications]({PREFIX}/applications.pdf) and [non-submitted historical archive]({PREFIX}/archive-v144.pdf) remain separate. No other paper is part of the principal submission.

Ballico 1993: the publisher's first page has now been inspected, but the complete theorem/proof text has not been obtained. The six-axis full-text comparison remains open. No editorial acceptance or exhaustive priority clearance is asserted.
''')

def assemble():
    if not BASE.is_dir(): raise RuntimeError('Immutable v146 directory is missing')
    # Never overwrite an overlay already supplied on this branch.
    for p in BASE.rglob('*'):
        rel=p.relative_to(BASE)
        if is_source(p,rel):
            dest=HERE/rel
            if not dest.exists():
                dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    hist=HERE/'history/v146-root';hist.mkdir(parents=True,exist_ok=True)
    records={}
    for p in BASE.rglob('*'):
        rel=p.relative_to(BASE)
        if not is_source(p,rel): continue
        if len(rel.parts)==1:
            dest=hist/p.name
            if dest.exists() and sha(dest)!=sha(p): raise RuntimeError('Historical root differs: '+str(rel))
            if not dest.exists(): shutil.copy2(p,dest)
        else:
            dest=HERE/rel
            if not dest.exists() or sha(dest)!=sha(p): raise RuntimeError('Inherited source changed: '+str(rel))
        records[str(rel)]={'sha256':sha(p),'preserved_at':str(dest.relative_to(HERE))}
    root_entry=ROOT/'CURRENT_REVIEW_ENTRY.md'
    hist_entry=hist/'CURRENT_REVIEW_ENTRY_AT_V146.md'
    if root_entry.exists() and not hist_entry.exists(): shutil.copy2(root_entry,hist_entry)
    dump(HERE/'INHERITED_SOURCE_V147.json',{'predecessor_review_commit':REVIEW,'source_files':records})
    # Old root audit files remain byte-preserved in history; avoid ambiguous active ledgers.
    for p in list(HERE.iterdir()):
        if p.is_file() and p.suffix in {'.md','.json'} and (BASE/p.name).exists() and p.name!='README.md':
            p.unlink()
    put(HERE/'build.sh','#!/usr/bin/env bash\nset -euo pipefail\ncd "$(dirname "$0")"\nexport OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1\npython revision_v147.py build\n')
    entry()
    print('Assembled v147; preserved',len(records),'predecessor source files')

def build():
    os.chdir(HERE)
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
    names='exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact revision137_exact revision138_exact revision139_exact revision140_exact revision141_spectral_exact revision141_likelihood_exact revision142_exact revision143_critical_exact revision144_projective_exact'.split()
    scripts=['checks/'+s+'.py' for s in names]+['check_v145.py','check_v146.py','check_local_v146.py','check_v147.py']
    records=[]
    for script in scripts:
        print('Executing',script,flush=True)
        log=evidence/(Path(script).stem+'.log')
        with log.open('w') as f:
            run=subprocess.run([sys.executable,script],stdout=f,stderr=subprocess.STDOUT)
        records.append({'script':script,'sha256':sha(HERE/script),'returncode':run.returncode,'log':str(log.relative_to(HERE))})
        dump(evidence/'EXECUTED_CHECKS_V147.json',records)
        if run.returncode:
            print(log.read_text()[-12000:]);raise RuntimeError('Regression failed: '+script)
    for name in ('geometry','applications','archive-v144'):
        for ext in ('aux','out','toc'):(HERE/(name+'.'+ext)).unlink(missing_ok=True)
        for iteration in range(1,4):
            print('Native LaTeX',name,'pass',iteration,flush=True)
            log=evidence/(name+'-pass'+str(iteration)+'.log')
            with log.open('w') as f:
                run=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],stdout=f,stderr=subprocess.STDOUT)
            if run.returncode:
                print(log.read_text()[-12000:]);raise RuntimeError('LaTeX failed: '+name)
        aux=(HERE/(name+'.aux')).read_text()
        put(HERE/(name+'-labels.aux'),'\n'.join(l for l in aux.splitlines() if l.startswith('\\newlabel{') and not l.startswith('\\newlabel{tocindent'))+'\n')
        shutil.copy2(HERE/(name+'.log'),evidence/(name+'-final.log'))
    verify()

def verify():
    evidence=HERE/'evidence'
    text={n:expand(HERE/(n+'.tex'),HERE) for n in ('geometry','applications','archive-v144')}
    labels=lambda t:re.findall(r'\\label\{([^}]+)\}',t)
    refs=lambda t:set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',t))
    checks={}
    main=text['geometry'];old=expand(BASE/'geometry.tex',BASE)
    checks['principal_proofs_self_contained']=not(refs(main)-set(labels(main))) and '\\externaldocument' not in main
    checks['applications_references_resolve']=not(refs(text['applications'])-set(labels(main))-set(labels(text['applications'])))
    checks['archive_references_resolve']=not(refs(text['archive-v144'])-set(labels(text['archive-v144'])))
    for name,t in text.items():
        log=(evidence/(name+'-final.log')).read_text(errors='replace')
        checks[name+'_labels_unique']=len(labels(t))==len(set(labels(t)))
        checks[name+'_references_resolved']=not bool(re.search(r'(There were undefined references|Citation .+ undefined|Reference .+ undefined|multiply defined|Rerun to get cross-references)',log))
        checks[name+'_no_overfull_boxes']=not bool(re.search(r'Overfull \\[hv]box',log))
        checks[name+'_native_pdf_exists']=(HERE/(name+'.pdf')).is_file()
    inherited=json.loads((HERE/'INHERITED_SOURCE_V147.json').read_text())['source_files']
    checks['all_predecessor_source_bytes_preserved']=all((HERE/r['preserved_at']).is_file() and sha(HERE/r['preserved_at'])==r['sha256'] for r in inherited.values())
    checks['all_v146_part_files_unchanged']=all(sha(HERE/p.relative_to(BASE))==sha(p) for p in (BASE/'parts').rglob('*.tex'))
    pattern=r'\\begin\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}[\s\S]*?\\end\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}'
    oldblocks=re.findall(pattern,old);newblocks=re.findall(pattern,main)
    checks['all_v146_principal_math_blocks_retained']=not(Counter(oldblocks)-Counter(newblocks))
    checks['all_v146_principal_labels_retained']=set(labels(old))<=set(labels(main))
    checks['applications_and_archive_drivers_unchanged']=all(sha(HERE/n)==sha(BASE/n) for n in ('applications.tex','archive-v144.tex'))
    required={'prop:first-relation-orbit-v147','prop:first-relation-group-v147','lem:linear-preserver-v147','lem:actual-factor-descent-v147','thm:general-moving-coefficients-v147','ex:isotrivial-covers-v147','cor:pencil-group-scheme-v147'}
    checks['new_structural_results_in_principal_manuscript']=required<=set(labels(main))
    records=json.loads((evidence/'EXECUTED_CHECKS_V147.json').read_text())
    checks['twenty_four_scripts_pass']=len(records)==24 and all(r['returncode']==0 and sha(HERE/r['script'])==r['sha256'] for r in records)
    checks['new_exact_regressions_pass']=json.loads((evidence/'REVISION147_EXACT.json').read_text())['ok'] is True
    source=os.environ.get('A2_SOURCE_COMMIT','LOCAL-PREFLIGHT-NOT-REMOTE')
    source_manifest={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*')
        if is_source(p,p.relative_to(HERE)) and p.name not in GENERATED}
    pdfs={}
    for n in text:
        p=HERE/(n+'.pdf');info=subprocess.check_output(['pdfinfo',str(p)],text=True)
        pdfs[n]={'pages':int(re.search(r'^Pages:\s*(\d+)',info,re.M)[1]),'bytes':p.stat().st_size,'sha256':sha(p)}
    receipt={'revision':147,'source_commit':source,'controlling_review_commit':REVIEW,
        'all_checks_pass':all(checks.values()),'checks':checks,'executed_script_count':len(records),
        'executed_scripts':records,'pdfs':pdfs,'labels':{n:len(labels(t)) for n,t in text.items()},
        'preserved_predecessor_source_files':len(inherited),'preserved_principal_math_blocks':len(oldblocks),
        'proof_certified_by_computation':False,'Ballico_1993_first_page_inspected':True,
        'Ballico_1993_full_text_comparison_completed':False,'historical_priority_certified':False,
        'journal_acceptance_asserted':False}
    dump(evidence/'BUILD_RECEIPT_V147.json',receipt)
    dump(HERE/'NONDELETION_V147.json',{'source_commit':source,'predecessor_review_commit':REVIEW,
        'all_source_bytes_preserved':checks['all_predecessor_source_bytes_preserved'],
        'all_v146_parts_unchanged':checks['all_v146_part_files_unchanged'],
        'all_principal_math_blocks_retained':checks['all_v146_principal_math_blocks_retained'],
        'all_principal_labels_retained':checks['all_v146_principal_labels_retained'],
        'source_files':inherited,'preservation_is_not_proof_certification':True})
    dump(HERE/'PROVENANCE_MANIFEST_V147.json',{'source_commit':source,'sha256':source_manifest})
    dump(HERE/'SOURCE_LOCK_V147.json',{'revision':147,'source_commit':source,
        'controlling_review_commit':REVIEW,'principal_manuscript':'geometry.pdf',
        'separate_application':'applications.pdf','non_submitted_archive':'archive-v144.pdf',
        'receipt':'evidence/BUILD_RECEIPT_V147.json','all_checks_pass':receipt['all_checks_pass'],
        'historical_priority_certified':False})
    print(json.dumps(receipt,indent=2))
    if not receipt['all_checks_pass']: raise RuntimeError('v147 audit failed')
    entry(source)

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in {'assemble','build','verify'}:
        raise SystemExit('Usage: revision_v147.py assemble|build|verify')
    globals()[sys.argv[1]]()
