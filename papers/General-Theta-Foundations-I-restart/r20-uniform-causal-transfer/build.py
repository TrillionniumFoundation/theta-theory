#!/usr/bin/env python3
"""Build immutable R20 and complete unchanged R19 (X), W, V, U, T and S."""
from __future__ import annotations
import argparse,json,sys,tempfile
from pathlib import Path
import native_build
from native_build import run
from verify import ROOT,require,verify,sha256
RETAINED_COMMIT='8ca6d78d06bd2a3dad366ff9e7a816d792a87f18'
RETAINED_TREE='ce14e0d57fef7aa415a4065cd3dac75172dd1efa'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--expected-tree');ap.add_argument('--output',default=str(ROOT/'artifacts'));ap.add_argument('--receipt',default=str(ROOT/'evidence'/'BUILD_RECEIPT.json'));args=ap.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);before=verify()
    with tempfile.TemporaryDirectory(prefix='theta-r20-full-') as td:
        td=Path(td);native=td/'native.json';retained=td/'retained.json';argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r19-effective-frontier'/'build.py'),'--source-sha',RETAINED_COMMIT,'--expected-tree',RETAINED_TREE,'--output',str(oldout),'--receipt',str(retained)])
        result=json.loads(native.read_text());previous=json.loads(retained.read_text());require(previous['native_source_tree_sha']==RETAINED_TREE,'retained R19 source binding changed')
        (out/'General_Theta_Foundations_I_R20_Companion_X.pdf').write_bytes((oldout/'General_Theta_Foundations_I_restart_R19.pdf').read_bytes())
        for letter in ('W','V','U','T','S'):
            (out/f'General_Theta_Foundations_I_R20_Companion_{letter}.pdf').write_bytes((oldout/f'General_Theta_Foundations_I_R19_Companion_{letter}.pdf').read_bytes())
        result.update(component='General Theta Foundations I restart R20 uniform causal transfer',retained_R19_and_complete_W_V_U_T_S=previous,total_isolated_pdf_builds=previous['total_isolated_pdf_builds']+2,technical_pdf_builds=previous['technical_pdf_builds']+2,cover_pdf_builds=previous['cover_pdf_builds'],retained_companion_X_is_unchanged_R19=True)
        from pypdf import PdfReader
        result['delivery_pdfs']={p.name:{'sha256':sha256(p.read_bytes()),'pages':len(PdfReader(p).pages),'bytes':p.stat().st_size} for p in sorted(out.glob('*.pdf'))}
        result['limitations']='Complete R20 and unchanged R19/W/V/U/T/S, not all repository papers. Nested regressions are distinct, not summed as independent checks. Delivery and exact finite checks do not prove continuous mathematics or priority.'
        require(verify()==before,'full build mutated source')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
