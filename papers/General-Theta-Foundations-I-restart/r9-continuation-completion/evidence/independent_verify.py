#!/usr/bin/env python3
"""Rebuild downloaded, source-bound R9 files without modifying the input packet."""
import argparse, hashlib, json, os, subprocess, sys, unicodedata
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(root):
    return {p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
def normalized(pdf):
    text=subprocess.check_output(['pdftotext','-enc','UTF-8',str(pdf),'-'],text=True)
    return ''.join(unicodedata.normalize('NFKC',text).split())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--source',required=True);ap.add_argument('--artifact',required=True);args=ap.parse_args()
    root=args.root.resolve();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    p=root/'papers/General-Theta-Foundations-I-restart/r9-continuation-completion'
    hosted=json.loads((p/'evidence/BUILD_RECEIPT.json').read_text())
    if hosted['source_commit']!=args.source:raise RuntimeError('source binding mismatch')
    before=snapshot(root)
    (out/'INPUT_HASHES_BEFORE.json').write_text(json.dumps(before,sort_keys=True,indent=2)+'\n')
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    for name in ('GITHUB_RUN_ID','HOSTED_RUN_ID','SOURCE_COMMIT'):env.pop(name,None)
    cmd=[sys.executable,str(p/'build.py'),'--source-sha',args.source,'--expected-tree','bffa275cd54758ac318d4eafa8d8c83be80c7b85','--output',str(out/'artifacts'),'--receipt',str(out/'INDEPENDENT_BUILD_RECEIPT.json')]
    with (out/'INDEPENDENT_BUILD.log').open('w') as f:
        result=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
    if result.returncode:raise RuntimeError('independent build failed; see log')
    after=snapshot(root)
    if before!=after:raise RuntimeError('downloaded source packet changed during rebuild')
    from pypdf import PdfReader
    comparisons={}
    for name in ('General_Theta_Foundations_I_restart_r9.pdf','General_Theta_Foundations_I_Supplement_S.pdf','General_Theta_Foundations_I_retained_technical_text.pdf'):
        a=p/'artifacts'/name;b=out/'artifacts'/name
        ta,tb=normalized(a),normalized(b)
        comparisons[name]={'hosted_sha256':sha(a),'independent_sha256':sha(b),'byte_identical_across_environments':sha(a)==sha(b),'normalized_text_identical':ta==tb,'normalized_text_sha256':hashlib.sha256(ta.encode()).hexdigest(),'hosted_pages':len(PdfReader(a).pages),'independent_pages':len(PdfReader(b).pages)}
        if ta!=tb or len(PdfReader(a).pages)!=len(PdfReader(b).pages):raise RuntimeError('cross-engine text/page mismatch: '+name)
    local=json.loads((out/'INDEPENDENT_BUILD_RECEIPT.json').read_text())
    if hosted['regression']!=local['regression']:raise RuntimeError('cross-environment finite regressions differ')
    verified={'status':'PASS','source_commit':args.source,'artifact_commit':args.artifact,'native_source_tree':'bffa275cd54758ac318d4eafa8d8c83be80c7b85','hosted_run_id':hosted['hosted_run_id'],'downloaded_input_files_unchanged':len(before),'source_mutation':False,'input_manifest_sha256':sha(out/'INPUT_HASHES_BEFORE.json'),'ordinary_and_optimized_equal_in_both_environments':True,'regression_outputs_identical_across_environments':True,'hosted_engine':hosted['tex_engine'],'independent_engine':local['tex_engine'],'isolated_pdf_builds_per_environment':6,'pdf_comparison':comparisons,'source_audit':local['source_audit'],'independent_receipt_sha256':sha(out/'INDEPENDENT_BUILD_RECEIPT.json'),'scope':'Complete R9 native source and supplied complete R6 technical text / Supplement S; not all repository historical papers; no claim that testing proves mathematics.'}
    (out/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(verified,sort_keys=True,indent=2)+'\n')
    print(json.dumps(verified,sort_keys=True,indent=2))
if __name__=='__main__':main()
