#!/usr/bin/env python3
"""Native stationary article plus all unchanged complete R34 mathematical companions."""
from __future__ import annotations
import argparse,json,sys,tempfile
from pathlib import Path
import native_build
from native_build import run
from verify import ROOT,require,verify,sha256
OLD_SOURCE='517112daa07e53228ec0ea9be8bac0187cd4db26'
OLD_TREE='eb89296ea9a5a1e3c42a08f573825ed86c21cd25'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--expected-tree');ap.add_argument('--output',default=str(ROOT/'artifacts'));ap.add_argument('--receipt',default=str(ROOT/'evidence/BUILD_RECEIPT.json'));args=ap.parse_args()
    before=verify();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    if args.source_sha:require(before['review_input_verified'],'published build requires pinned external R32 report')
    with tempfile.TemporaryDirectory(prefix='theta-r37-full-') as td:
        td=Path(td);native=td/'native.json';old=td/'retained.json';argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        current=json.loads(native.read_text());oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r34-bellman-acquisition/build.py'),'--source-sha',OLD_SOURCE,'--expected-tree',OLD_TREE,'--output',str(oldout),'--receipt',str(old)])
        previous=json.loads(old.read_text());require(previous['ordinary_source_projection_tree_sha']==OLD_TREE,'historical source mismatch')
        (out/'General_Theta_Foundations_I_R37_Companion_I.pdf').write_bytes((oldout/'General_Theta_Foundations_I_restart_R34.pdf').read_bytes())
        for letter in ('H','G','F','E','D','C','B','A','X','W','V','U','T','S'):
            (out/f'General_Theta_Foundations_I_R37_Companion_{letter}.pdf').write_bytes((oldout/f'General_Theta_Foundations_I_R34_Companion_{letter}.pdf').read_bytes())
        current.update(component='General Theta Foundations I restart R37 stationary acquired geometry',retained_complete_R34=previous,total_isolated_pdf_builds=previous['total_isolated_pdf_builds']+2,technical_pdf_builds=previous['technical_pdf_builds']+2,cover_pdf_builds=previous['cover_pdf_builds'],original_R34_unchanged=True)
        from pypdf import PdfReader
        current['delivery_pdfs']={p.name:{'sha256':sha256(p.read_bytes()),'pages':len(PdfReader(p).pages),'bytes':p.stat().st_size,'normalized_text_sha256':sha256(' '.join(run(['pdftotext','-enc','UTF-8',str(p),'-']).split()).encode())} for p in sorted(out.glob('*.pdf'))}
        current['total_delivery_pages']=sum(x['pages'] for x in current['delivery_pdfs'].values())
        current['limitations']='Native R37 plus complete R34 as I, R32 as H and all previous companions. Original R27 and corrected F remain distinct. Not every historical paper. Finite tests/builds are not continuum proofs, priority, importance or acceptance certificates.'
        require(verify()==before,'ordinary source changed during full build')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(current,sort_keys=True,indent=2)+'\n');print(json.dumps(current,sort_keys=True,indent=2))
if __name__=='__main__':main()
