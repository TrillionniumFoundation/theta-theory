#!/usr/bin/env python3
"""Build new article plus complete, immutable mathematical Supplements T and S."""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path
import native_build
from supplement_build import cover_and_attach
from verify import ROOT, require, verify
RETAINED_COMMIT='6b9677c4444d8b57386d024473a550f0a2b57a27'
RETAINED_TREE='7378579e02b0f0e51876f560b2fc1cfc0a3a3579'

def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    require(p.returncode==0,'command failed: '+repr(args)+'\n'+p.stdout[-16000:])
    return p.stdout

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-sha');ap.add_argument('--expected-tree')
    ap.add_argument('--output',default=str(ROOT/'artifacts'))
    ap.add_argument('--receipt',default=str(ROOT/'evidence'/'BUILD_RECEIPT.json'))
    args=ap.parse_args();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    before=verify()
    with tempfile.TemporaryDirectory(prefix='theta-r11-full-') as tmp:
        tmp=Path(tmp);native=tmp/'native.json';retained=tmp/'retained.json'
        argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        (out/'LATEX_BUILD.log').rename(out/'R11_LATEX_BUILD.log')
        oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r10-adaptive-completion'/'build.py'),
             '--source-sha',RETAINED_COMMIT,'--expected-tree',RETAINED_TREE,
             '--output',str(oldout),'--receipt',str(retained)])
        result=json.loads(native.read_text());old=json.loads(retained.read_text())
        require(old['native_source_tree_sha']==RETAINED_TREE,'retained source changed')
        result['retained_article_and_supplement_S']=old
        result['supplement_T']=cover_and_attach(oldout/'General_Theta_Foundations_I_restart_r10.pdf',
                                               out/'General_Theta_Foundations_I_Supplement_T.pdf')
        (out/'General_Theta_Foundations_I_Supplement_S.pdf').write_bytes(
            (oldout/'General_Theta_Foundations_I_Supplement_S.pdf').read_bytes())
        result['total_isolated_pdf_builds']=10
        result['technical_pdf_builds']=6;result['cover_pdf_builds']=4
        result['component']='General Theta Foundations I restart R11 posterior pooling'
        result['limitations']='Complete R11 article, complete R10 as Supplement T and complete R6 as Supplement S; not every historical paper. Regressions do not certify continuum proofs or priority.'
        require(verify()==before,'source mutation during complete build')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True)
        rp.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
