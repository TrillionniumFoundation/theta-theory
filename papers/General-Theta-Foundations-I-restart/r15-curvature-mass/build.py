#!/usr/bin/env python3
"""Build the native R15 and unchanged complete Supplements U, T and S."""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import native_build
from supplement_build import cover_and_attach
from verify import ROOT, require, verify
RETAINED_COMMIT='6ef290d21064b1e6514b343d3d451ad0a77e0c04'
RETAINED_TREE='f37f42455e99419d118156ecb122d9826e651c2d'
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
    with tempfile.TemporaryDirectory(prefix='theta-r15-full-') as tmp:
        tmp=Path(tmp);native=tmp/'native.json';retained=tmp/'retained.json'
        argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        (out/'LATEX_BUILD.log').rename(out/'R15_LATEX_BUILD.log')
        oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r11-posterior-pooling'/'build.py'),
             '--source-sha',RETAINED_COMMIT,'--expected-tree',RETAINED_TREE,
             '--output',str(oldout),'--receipt',str(retained)])
        result=json.loads(native.read_text());old=json.loads(retained.read_text())
        require(old['native_source_tree_sha']==RETAINED_TREE,'retained source changed')
        result['retained_article_and_supplements_T_S']=old
        result['supplement_U']=cover_and_attach(oldout/'General_Theta_Foundations_I_restart_r11.pdf',
                                               out/'General_Theta_Foundations_I_Supplement_U.pdf')
        for letter in ['T','S']:
            name='General_Theta_Foundations_I_Supplement_'+letter+'.pdf'
            (out/name).write_bytes((oldout/name).read_bytes())
        result.update(total_isolated_pdf_builds=14,technical_pdf_builds=8,cover_pdf_builds=6,
            component='General Theta Foundations I restart R15 acquired mass and charged clocks',
            limitations='Complete R15 and complete inherited U/T/S; not every historical paper. Finite regressions do not prove continuum mathematics or priority.')
        require(verify()==before,'source mutation during complete build')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True)
        rp.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
