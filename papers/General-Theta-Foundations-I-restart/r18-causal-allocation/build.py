#!/usr/bin/env python3
"""Build immutable R18 and complete unchanged R15 (V), U, T and S."""
from __future__ import annotations
import argparse,json,sys,tempfile
from pathlib import Path
import native_build
from native_build import run
from verify import ROOT,require,verify,sha256
RETAINED_COMMIT='0f391dd67b2fc8d47685e91d86253898451e2730'
RETAINED_TREE='1447a5858bbb75d35367299df5f9f24362e89904'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--expected-tree');ap.add_argument('--output',default=str(ROOT/'artifacts'));ap.add_argument('--receipt',default=str(ROOT/'evidence'/'BUILD_RECEIPT.json'));args=ap.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);before=verify()
    with tempfile.TemporaryDirectory(prefix='theta-r18-full-') as td:
        td=Path(td);native=td/'native.json';retained=td/'retained.json';argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r15-curvature-mass'/'build.py'),'--source-sha',RETAINED_COMMIT,'--expected-tree',RETAINED_TREE,'--output',str(oldout),'--receipt',str(retained)])
        result=json.loads(native.read_text());old=json.loads(retained.read_text());require(old['native_source_tree_sha']==RETAINED_TREE,'retained R15 source binding changed')
        (out/'General_Theta_Foundations_I_R18_Companion_V.pdf').write_bytes((oldout/'General_Theta_Foundations_I_restart_r15.pdf').read_bytes())
        for letter in ('U','T','S'):
            (out/f'General_Theta_Foundations_I_R18_Companion_{letter}.pdf').write_bytes((oldout/f'General_Theta_Foundations_I_Supplement_{letter}.pdf').read_bytes())
        result.update(component='General Theta Foundations I restart R18 causal allocation',retained_R15_and_complete_U_T_S=old,total_isolated_pdf_builds=16,technical_pdf_builds=10,cover_pdf_builds=6,retained_companion_V_is_unchanged_R15=True)
        from pypdf import PdfReader
        result['delivery_pdfs']={p.name:{'sha256':sha256(p.read_bytes()),'pages':len(PdfReader(p).pages),'bytes':p.stat().st_size} for p in sorted(out.glob('*.pdf'))}
        result['limitations']='Complete R18 and complete retained R15/U/T/S, not all repository papers. Native and nested retained regressions are separate. Delivery checks do not prove continuum mathematics or priority.'
        require(verify()==before,'full build mutated source')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
