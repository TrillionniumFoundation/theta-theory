#!/usr/bin/env python3
"""Read-only full R25 build and the complete unchanged R24 archival packet."""
from __future__ import annotations
import argparse,json,sys,tempfile
from pathlib import Path
import native_build
from native_build import run
from verify import ROOT,require,verify,sha256
OLD_SOURCE='5cb42423f8ea62139bd51093a5b6ba69379337b4'
OLD_TREE='c5a5a0c63abf76f4535c544ce75f82ee93b14c7f'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--expected-tree');ap.add_argument('--output',default=str(ROOT/'artifacts'));ap.add_argument('--receipt',default=str(ROOT/'evidence'/'BUILD_RECEIPT.json'));args=ap.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);before=verify()
    with tempfile.TemporaryDirectory(prefix='theta-r25-full-') as td:
        td=Path(td);native=td/'native.json';old=td/'retained.json';argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        run([sys.executable,str(ROOT/'regression.py'),'--output',str(out/'certificate')])
        oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r24-renewal-geometry'/'build.py'),'--source-sha',OLD_SOURCE,'--expected-tree',OLD_TREE,'--output',str(oldout),'--receipt',str(old)])
        current=json.loads(native.read_text());previous=json.loads(old.read_text());require(previous['native_source_tree_sha']==OLD_TREE,'retained source changed')
        (out/'General_Theta_Foundations_I_R25_Companion_C.pdf').write_bytes((oldout/'General_Theta_Foundations_I_restart_R24.pdf').read_bytes())
        for letter in ('B','A','X','W','V','U','T','S'):
            (out/f'General_Theta_Foundations_I_R25_Companion_{letter}.pdf').write_bytes((oldout/f'General_Theta_Foundations_I_R24_Companion_{letter}.pdf').read_bytes())
        current.update(component='General Theta Foundations I restart R25 retained-state causal transfer',retained_complete_R24=previous,total_isolated_pdf_builds=previous['total_isolated_pdf_builds']+2,technical_pdf_builds=previous['technical_pdf_builds']+2,cover_pdf_builds=previous['cover_pdf_builds'],retained_companions_unchanged=True)
        from pypdf import PdfReader
        current['delivery_pdfs']={p.name:{'sha256':sha256(p.read_bytes()),'pages':len(PdfReader(p).pages),'bytes':p.stat().st_size} for p in sorted(out.glob('*.pdf'))}
        current['limitations']='Complete native R25 and unchanged R24/B/A/X/W/V/U/T/S; not every historical paper. Nested test counts are not summed. Builds are not continuum proof or priority certificates.'
        require(verify()==before,'source changed in build')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(current,sort_keys=True,indent=2)+'\n');print(json.dumps(current,sort_keys=True,indent=2))
if __name__=='__main__':main()
