#!/usr/bin/env python3
"""Build the principal v4 manuscript and run only its explicitly named new suite.
Historical tests/receipts inherited with the repository are not counted.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,platform,re,shutil,subprocess,sys
from pathlib import Path

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def run(command:list[str],cwd:Path,log:Path)->str:
    completed=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
    log.write_text(completed.stdout)
    if completed.returncode:
        raise RuntimeError(f'Command failed ({completed.returncode}); inspect {log}: {command}')
    return completed.stdout

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--render',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parent;validation=root/'validation';validation.mkdir(exist_ok=True)
    if shutil.which('latexmk') is None:raise RuntimeError('latexmk is required; install a TeX distribution before building.')
    try:import fitz
    except ImportError as exc:raise RuntimeError('PyMuPDF is required for PDF verification.') from exc
    run([sys.executable,'tests/test_v4.py'],root,validation/'V4_TEST_OUTPUT.txt')
    run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','main.tex'],root,validation/'V4_LATEX_OUTPUT.txt')
    log=(root/'main.log').read_text(errors='replace')
    fatal_patterns={'overfull_boxes':r'Overfull \\[hv]box','undefined_reference_or_citation':r'(?:Reference|Citation) .+ undefined',
                    'undefined_references_summary':r'There were undefined references','multiply_defined_labels':r'multiply defined'}
    issues={key:len(re.findall(pattern,log)) for key,pattern in fatal_patterns.items()}
    if any(issues.values()):raise RuntimeError(f'PDF preflight failed: {issues}')
    doc=fitz.open(root/'main.pdf');outside=[]
    for i,page in enumerate(doc):
        for word in page.get_text('words'):
            x0,y0,x1,y1=word[:4]
            if x0<-.5 or y0<-.5 or x1>page.rect.width+.5 or y1>page.rect.height+.5:
                outside.append({'page':i+1,'word':word[4]})
    if outside:raise RuntimeError(f'Text outside the PDF page: {outside[:10]}')
    if args.render:
        out=validation/'rendered_pages';out.mkdir(exist_ok=True)
        for i,page in enumerate(doc):page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(out/f'page-{i+1:03d}.png')
    source_paths=[root/'main.tex',root/'references.tex']+sorted((root/'sections').glob('*.tex'))
    receipt={'edition':'A1 English revision 4.0','executed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'principal_only':True,'foundation_companion_rebuilt':False,'historical_test_counts_included':False,
        'python':platform.python_version(),'compiler':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
        'pages':len(doc),'pdf_bytes':(root/'main.pdf').stat().st_size,'pdf_sha256':digest(root/'main.pdf'),
        'checks':issues,'text_outside_page':len(outside),
        'underfull_box_warnings':len(re.findall(r'Underfull \\[hv]box',log)),
        'source_sha256':{str(p.relative_to(root)):digest(p) for p in source_paths},
        'test_receipt_sha256':digest(validation/'V4_CHECKS.json'),
        'adaptive_certificate_sha256':digest(validation/'ADAPTIVE_CERTIFICATE.json'),
        'rendered_this_run':args.render,'visual_review':'See V4_VISUAL_REVIEW.md; rendering alone is not visual inspection.'}
    (validation/'V4_BUILD.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
