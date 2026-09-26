#!/usr/bin/env python3
"""Read-only qualification of the actual committed submission, rebuilt in a temp copy."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REL=HERE.relative_to(ROOT)
NAMES=('reconstruction','divisor-geometry','technical-supplement','geometry')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def text_of(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'])
def run(argv,log):
    with log.open('w') as out:
        p=subprocess.run(argv,stdout=out,stderr=subprocess.STDOUT)
    require(p.returncode==0,'Read-only rebuild failed; inspect '+str(log))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output.resolve()
    require(ROOT not in out.parents and out!=ROOT,'Qualification output must be outside checkout')
    out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    expected=json.loads((HERE/'BUILD_RECEIPT_V171.json').read_text())
    require(expected['compiled'] and expected['inherited_v170_full_chain_rerun'],'Submission was not fully built')
    originals={}
    for n in NAMES:
        for ext in ('tex','pdf'):
            p=HERE/(n+'.'+ext);require(sha(p)==expected['outputs'][n][ext+'_sha256'],'Committed object hash mismatch '+str(p))
        originals[n]={'tex':(HERE/(n+'.tex')).read_bytes(),'text':text_of(HERE/(n+'.pdf'))}
    for n,h in expected['authored_source_sha256'].items():
        require(sha(HERE/n)==h,'Authored source mismatch '+n)
    for n,h in expected.get('supporting_document_sha256',{}).items():
        require(sha(HERE/n)==h,'Supporting document mismatch '+n)
    old_hashes={n:sha(HERE.parent/'v170'/(n+'.tex')) for n in expected['predecessor_tex_sha256']}
    require(old_hashes==expected['predecessor_tex_sha256'],'Historical source mismatch')
    with tempfile.TemporaryDirectory(prefix='a2-v171-read-only-') as temp:
        work=Path(temp)
        # Only copy the source families needed by the inherited check chain.
        # No repository file is generated, committed, staged or otherwise modified.
        suffixes={'.py','.tex','.md','.json','.bib','.sty','.cls','.sh'}
        article=ROOT/'papers/A2-v17-boundary-information-coarsening/article'
        files=[p for p in article.rglob('*') if p.is_file() and p.suffix in suffixes]
        files += [p for p in (ROOT/'scripts').rglob('*') if p.is_file() and p.suffix in suffixes] if (ROOT/'scripts').exists() else []
        files += [ROOT/'reviews/a2-v170-independent-harsh-top4-2026-09-27/REFEREE_REPORT.md']
        for p in files:
            dst=work/p.relative_to(ROOT);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
        target=work/REL
        run([sys.executable,str(target/'check_v171.py')],out/'exact-check-command.log')
        run([sys.executable,str(target/'assemble_v171.py'),'--build'],out/'compile-command.log')
        actual=json.loads((target/'BUILD_RECEIPT_V171.json').read_text())
        require(actual['compiled'] and actual['inherited_v170_full_chain_rerun'],'Incomplete exact-tip rebuild')
        require(actual['predecessor_math_blocks']==487 and actual['current_math_blocks']==expected['current_math_blocks'],'Math preservation count mismatch')
        require(actual['papers_plus_supplement_partition_master'] and not actual['missing_labels'] and not actual['duplicate_labels'],'Proof or label preservation failure')
        comparisons={}
        for n in NAMES:
            require((target/(n+'.tex')).read_bytes()==originals[n]['tex'],'Regenerated standalone source mismatch '+n)
            require(text_of(target/(n+'.pdf'))==originals[n]['text'],'Recompiled PDF text/layout mismatch '+n)
            require(actual['outputs'][n]['pages']==expected['outputs'][n]['pages'],'Page count mismatch '+n)
            comparisons[n]={'standalone_source_identical':True,'pdf_layout_text_identical':True,
                'pdf_bytes_identical':sha(target/(n+'.pdf'))==expected['outputs'][n]['pdf_sha256'],
                'submitted_pdf_sha256':expected['outputs'][n]['pdf_sha256'],
                'rebuilt_pdf_sha256':sha(target/(n+'.pdf')),'pages':actual['outputs'][n]['pages']}
        for filename in ('BUILD_RECEIPT_V171.json','EXACT_CHECKS_V171.json','NONDELETION_V171.json','THEOREM_INDEX_V171.json'):
            shutil.copy2(target/filename,out/('REBUILT_'+filename))
    # Confirm that even the originally read bytes have not changed during qualification.
    for n in NAMES:
        require((HERE/(n+'.tex')).read_bytes()==originals[n]['tex'],'Checkout source changed '+n)
        require(sha(HERE/(n+'.pdf'))==expected['outputs'][n]['pdf_sha256'],'Checkout PDF changed '+n)
    for n,h in old_hashes.items():require(sha(HERE.parent/'v170'/(n+'.tex'))==h,'Historical checkout changed '+n)
    result={'revision':171,'qualified_sha':os.environ.get('GITHUB_SHA','local-read-only-verification'),
        'run_id':os.environ.get('GITHUB_RUN_ID'),'read_only':True,'all_checks_pass':True,
        'inherited_chain_rerun':True,'submitted_hashes_verified':True,
        'all_predecessor_math_blocks_retained':487,'recompiled_outputs':comparisons,
        'branch_protection_enforcement_not_inferred':True,
        'qualification_does_not_certify_general_proofs':True,
        'duration_seconds':round(time.monotonic()-start,3)}
    (out/'READ_ONLY_QUALIFICATION_V171.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
