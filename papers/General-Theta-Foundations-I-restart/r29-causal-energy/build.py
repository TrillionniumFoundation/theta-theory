#!/usr/bin/env python3
"""Complete new manuscript, corrected full companion, and immutable historical rebuild."""
from __future__ import annotations
import argparse,json,os,re,shutil,sys,tempfile
from pathlib import Path
import native_build
from native_build import run
from verify import ROOT,require,verify,sha256,tex_audit
OLD_SOURCE='4a9f9a36f6ad02561f8e8eae112674f3f3c5d777';OLD_TREE='36c91366f880989e6e2836d7e7bf55e6666d4953'
def companion(output:Path)->dict:
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1791590400',FORCE_SOURCE_DATE='1',TZ='UTC',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    origin=ROOT/'retained/companion_f';audit=tex_audit(origin);products=[]
    for _ in range(2):
        with tempfile.TemporaryDirectory(prefix='theta-r29-companion-') as td:
            work=Path(td);shutil.copytree(origin,work/'source');src=work/'source';out=work/'out';out.mkdir()
            for __ in range(3):run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-recorder','-output-directory='+str(out),'main.tex'],cwd=src,env=env)
            log=(out/'main.log').read_text(errors='replace')
            for bad in ('There were undefined references','There were multiply-defined labels','Citation `','Reference `','Overfull \\hbox','Overfull \\vbox'):require(bad not in log,'corrected companion '+bad)
            loaded=set()
            for line in (out/'main.fls').read_text().splitlines():
                if line.startswith('INPUT '):
                    p=Path(line[6:]);p=p if p.is_absolute() else src/p
                    try:rel=p.resolve().relative_to(src).as_posix()
                    except ValueError:continue
                    if rel.endswith('.tex'):loaded.add(rel)
            require(loaded==set(audit['active_tex']),'companion input list')
            txt=' '.join(run(['pdftotext','-enc','UTF-8',str(out/'main.pdf'),'-']).split())
            pages=int(re.search(r'^Pages:\s+(\d+)',run(['pdfinfo',str(out/'main.pdf')]),re.M).group(1))
            products.append(((out/'main.pdf').read_bytes(),txt,pages,log))
    require(products[0][0]==products[1][0],'companion repeat bytes differ')
    data,text,pages,log=products[0];(output/'General_Theta_Foundations_I_R29_Companion_F.pdf').write_bytes(data);(output/'COMPANION_F_LATEX.log').write_text(log)
    return {'status':'PASS','pages':pages,'sha256':sha256(data),'normalized_text_sha256':sha256(text.encode()),'source_audit':audit,'isolated_builds':2,'passes_per_build':3,'within_environment_byte_equal':True,'scope':'complete R27 mathematical text in a new correction copy; original subtree unchanged'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--expected-tree');ap.add_argument('--output',default=str(ROOT/'artifacts'));ap.add_argument('--receipt',default=str(ROOT/'evidence/BUILD_RECEIPT.json'));args=ap.parse_args()
    before=verify();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    if args.source_sha:require(before['review_input_verified'],'published build must contain pinned external report')
    with tempfile.TemporaryDirectory(prefix='theta-r29-full-') as td:
        td=Path(td);native=td/'native.json';old=td/'retained.json';argv=sys.argv[:]
        sys.argv=['native_build.py','--output',str(out),'--receipt',str(native)]
        if args.source_sha:sys.argv+=['--source-sha',args.source_sha]
        if args.expected_tree:sys.argv+=['--expected-tree',args.expected_tree]
        try:native_build.main()
        finally:sys.argv=argv
        run([sys.executable,str(ROOT/'regression.py'),'--output',str(out/'certificate')])
        current=json.loads(native.read_text());current['corrected_companion_f']=companion(out)
        oldout=out/'retained';oldout.mkdir(exist_ok=True)
        run([sys.executable,str(ROOT.parent/'r27-occupation-modulus/build.py'),'--source-sha',OLD_SOURCE,'--expected-tree',OLD_TREE,'--output',str(oldout),'--receipt',str(old)])
        previous=json.loads(old.read_text());require(previous['native_source_tree_sha']==OLD_TREE,'historical source mismatch')
        # Confirm every original R27 TeX input against the declared correction baseline.
        patches=json.loads((ROOT/'RETAINED_PATCHES.json').read_text())
        for name,item in patches['files'].items():require(sha256((ROOT.parent/'r27-occupation-modulus'/name).read_bytes())==item['original_sha256'],'original R27 changed '+name)
        original_labels=set();retained_labels=set()
        for name in patches['files']:
            original_labels.update(re.findall(r'\\label\{([^}]+)\}',(ROOT.parent/'r27-occupation-modulus'/name).read_text()))
            retained_labels.update(re.findall(r'\\label\{([^}]+)\}',(ROOT/'retained/companion_f'/name).read_text()))
        require(original_labels <= retained_labels,'a retained mathematical label was removed')
        current['retained_original_labels_preserved']=len(original_labels)
        for letter in ('E','D','C','B','A','X','W','V','U','T','S'):
            (out/f'General_Theta_Foundations_I_R29_Companion_{letter}.pdf').write_bytes((oldout/f'General_Theta_Foundations_I_R27_Companion_{letter}.pdf').read_bytes())
        current.update(component='General Theta Foundations I restart R29 causal energy and homogeneous acquired geometry',retained_complete_R27=previous,total_isolated_pdf_builds=previous['total_isolated_pdf_builds']+4,technical_pdf_builds=previous['technical_pdf_builds']+4,cover_pdf_builds=previous['cover_pdf_builds'],original_R27_unchanged=True)
        from pypdf import PdfReader
        current['delivery_pdfs']={p.name:{'sha256':sha256(p.read_bytes()),'pages':len(PdfReader(p).pages),'bytes':p.stat().st_size} for p in sorted(out.glob('*.pdf'))}
        current['limitations']='New native, full corrected companion F, and complete inherited E/D/C/B/A/X/W/V/U/T/S. Original R27 is independently rebuilt too. Not every historical paper. Checks are not mathematical proofs or priority certificates.'
        require(verify()==before,'source changed during full build')
        rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(current,sort_keys=True,indent=2)+'\n');print(json.dumps(current,sort_keys=True,indent=2))
if __name__=='__main__':main()
