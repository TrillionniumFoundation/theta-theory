#!/usr/bin/env python3
"""New Bayesian article and complete retained R29 packet, with a correction-title cover."""
from __future__ import annotations
import argparse,io,json,os,re,shutil,sys,tempfile
from pathlib import Path
import native_build
from native_build import run
from verify import ROOT,require,verify,sha256
OLD_SOURCE='31d06e6f21ccfe072016a7f0c9d39aeee4f6836f'
OLD_TREE='8e7a5a5ba3cb01124005a3c7a032197759a88e66'
def correction_cover(out:Path,original:Path)->dict:
    from pypdf import PdfReader,PdfWriter
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1791676800',FORCE_SOURCE_DATE='1',TZ='UTC',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    products=[]
    for _ in range(2):
        with tempfile.TemporaryDirectory(prefix='theta-r32-f-notice-') as td:
            work=Path(td);shutil.copyfile(ROOT/'companion_f_notice.tex',work/'main.tex')
            for __ in range(3):run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=work,env=env)
            log=(work/'main.log').read_text(errors='replace')
            for bad in ('There were undefined references','Overfull \\hbox','Overfull \\vbox'):require(bad not in log,'correction-cover audit '+bad)
            require(len(PdfReader(work/'main.pdf').pages)==1,'correction notice must be one page')
            products.append((work/'main.pdf').read_bytes())
    require(products[0]==products[1],'correction notice repeat differs')
    cover=out/'R32_Companion_F_notice.pdf';cover.write_bytes(products[0])
    merged=[]
    for _ in range(2):
        writer=PdfWriter();writer.append(str(cover));writer.append(str(original))
        writer.add_metadata({'/Title':'Corrected preserved R27 article: Companion F','/Author':'Qian Qi','/Subject':'R32 cover notice followed by the complete corrected R29 Companion F; not the original R27 review object'})
        buf=io.BytesIO();writer.write(buf);merged.append(buf.getvalue())
    require(merged[0]==merged[1],'companion F deterministic merge mismatch')
    target=out/'General_Theta_Foundations_I_R32_Companion_F.pdf';target.write_bytes(merged[0])
    require(len(PdfReader(target).pages)==len(PdfReader(original).pages)+1,'retained companion page loss')
    # The original body is appended, not regenerated or text-replaced.
    a=PdfReader(original);b=PdfReader(target)
    for i in range(len(a.pages)):
        require(' '.join((a.pages[i].extract_text() or '').split())==' '.join((b.pages[i+1].extract_text() or '').split()),'companion F body text changed')
    cover.unlink()
    return {'status':'PASS','notice_pages':1,'original_corrected_pages':len(a.pages),'delivery_pages':len(b.pages),'original_corrected_pdf_sha256':sha256(original.read_bytes()),'notice_sha256':sha256(products[0]),'delivery_sha256':sha256(target.read_bytes()),'isolated_notice_builds':2,'passes_per_build':3,'within_environment_byte_equal':True,'all_retained_body_page_texts_equal':True,'two_independent_merges_byte_equal':True,'original_R27_source_and_report':'preserved separately, not overwritten','scope':'one explicit title-page notice, followed by all pages of corrected Companion F rebuilt by the retained R29 pipeline'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--expected-tree');ap.add_argument('--output',default=str(ROOT/'artifacts'));ap.add_argument('--receipt',default=str(ROOT/'evidence/BUILD_RECEIPT.json'));args=ap.parse_args()
    before=verify();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    if args.source_sha:require(before['review_input_verified'],'published build requires pinned external R29 report')
    with tempfile.TemporaryDirectory(prefix='theta-r32-full-') as td:
        td=Path(td);native=td/'native.json';old=td/'retained.json';argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        current=json.loads(native.read_text())
        oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r29-causal-energy/build.py'),'--source-sha',OLD_SOURCE,'--expected-tree',OLD_TREE,'--output',str(oldout),'--receipt',str(old)])
        previous=json.loads(old.read_text());require(previous['ordinary_source_projection_tree_sha']==OLD_TREE,'historical source mismatch')
        (out/'General_Theta_Foundations_I_R32_Companion_G.pdf').write_bytes((oldout/'General_Theta_Foundations_I_restart_R29.pdf').read_bytes())
        for letter in ('E','D','C','B','A','X','W','V','U','T','S'):
            (out/f'General_Theta_Foundations_I_R32_Companion_{letter}.pdf').write_bytes((oldout/f'General_Theta_Foundations_I_R29_Companion_{letter}.pdf').read_bytes())
        current['corrected_companion_f_notice']=correction_cover(out,oldout/'General_Theta_Foundations_I_R29_Companion_F.pdf')
        current.update(component='General Theta Foundations I restart R32 Bayesian causal acquired geometry',retained_complete_R29=previous,total_isolated_pdf_builds=previous['total_isolated_pdf_builds']+4,technical_pdf_builds=previous['technical_pdf_builds']+2,cover_pdf_builds=previous['cover_pdf_builds']+2,original_R29_unchanged=True)
        from pypdf import PdfReader
        current['delivery_pdfs']={p.name:{'sha256':sha256(p.read_bytes()),'pages':len(PdfReader(p).pages),'bytes':p.stat().st_size,'normalized_text_sha256':sha256(' '.join(run(['pdftotext','-enc','UTF-8',str(p),'-']).split()).encode())} for p in sorted(out.glob('*.pdf'))}
        current['total_delivery_pages']=sum(x['pages'] for x in current['delivery_pdfs'].values())
        current['limitations']='Native R32, complete R29 article as G, full corrected F with one explicit correction-title cover, and complete E/D/C/B/A/X/W/V/U/T/S. Not every historical paper. Finite checks and builds do not certify continuum proofs, novelty or external acceptance.'
        require(verify()==before,'ordinary source changed during full build')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(current,sort_keys=True,indent=2)+'\n');print(json.dumps(current,sort_keys=True,indent=2))
if __name__=='__main__':main()
