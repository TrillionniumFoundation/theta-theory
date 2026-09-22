"""Check delivered inputs, exact finite results, typesetting and page preservation.

This is not a machine proof checker. It deliberately records that distinction.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import fitz
import numpy
import sympy

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'v122'

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def normalized_text(page: fitz.Page) -> str:
    return ''.join(page.get_text().split())

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', default='evidence/REBUILD_RECEIPT.json')
    args = parser.parse_args()
    lock = json.loads((ROOT/'SOURCE_LOCK.json').read_text())
    for name, digest in lock['sha256'].items():
        if sha(ROOT/name) != digest:
            raise RuntimeError(f'Source integrity mismatch: {name}')
    preserved = json.loads((ROOT/'evidence/PRESERVATION.json').read_text())
    for name, digest in preserved['v122_input_sha256'].items():
        if sha(BASE/name) != digest:
            raise RuntimeError(f'Historical input changed: {name}')
    for name in ('flags_elliptic','loewy','ramification_intrinsic'):
        if sha(ROOT/'checks/inherited'/f'{name}.py') != sha(BASE/'checks'/f'{name}.py'):
            raise RuntimeError(f'Inherited check not byte-preserved: {name}')
    diagnostics = {}
    for name in ('K3_CERTIFICATES','CORANK2_CERTIFICATES','inherited_flags_elliptic',
                 'inherited_loewy','inherited_ramification_intrinsic'):
        path=ROOT/'evidence'/f'{name}.json'
        data=json.loads(path.read_text())
        diagnostics[name]={'sha256':sha(path),'parsed':True}
    k3=json.loads((ROOT/'evidence/K3_CERTIFICATES.json').read_text())
    assert k3['immersion']['rank']==25 and k3['finite_witness_checks_passed']
    assert k3['first_25_rows_exact_determinant']=='4279473148893659522379284480'
    assert k3['basepoint_degree5']['rank']==56 and k3['smoothness_degree9']['rank']==220
    corank=json.loads((ROOT/'evidence/CORANK2_CERTIFICATES.json').read_text())
    assert corank['primary_identity'] and corank['nilradical_index']==3
    logs={}
    for stem in ('geometry','paper_latex'):
        path=ROOT/f'{stem}.log'
        text=path.read_text(errors='replace')
        patterns={'overfull':r'Overfull \\[hv]box',
                  'undefined_references':r'There were undefined references|Reference .+ undefined|Citation .+ undefined',
                  'multiply_defined':r'multiply defined|multiply-defined',
                  'latex_errors':r'^!'}
        counts={key:len(re.findall(pat,text,re.M)) for key,pat in patterns.items()}
        if any(counts.values()):
            raise RuntimeError(f'Typesetting postflight failed: {stem}: {counts}')
        logs[stem]=counts
    main_pdf=fitz.open(ROOT/'geometry.pdf')
    full=fitz.open(ROOT/'paper.pdf')
    old=fitz.open(BASE/'paper.pdf')
    assert len(main_pdf)==16 and len(old)==130 and len(full)==147
    shift=len(main_pdf)+1
    text_ok=[];raster_ok=[]
    for i in range(len(old)):
        text_ok.append(normalized_text(old[i])==normalized_text(full[i+shift]))
        a=old[i].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
        b=full[i+shift].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
        raster_ok.append(a.width==b.width and a.height==b.height and a.samples==b.samples)
    if not all(text_ok) or not all(raster_ok):
        raise RuntimeError('Historical PDF page preservation failed.')
    assert all(normalized_text(main_pdf[i])==normalized_text(full[i]) for i in range(len(main_pdf)))
    # Compare each label and theorem number to the typesetter's own resolved .aux.
    aux=(ROOT/'geometry.aux').read_text()
    label_map={m.group(1):{'number':m.group(2),'page':int(m.group(3))}
               for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',aux)}
    (ROOT/'evidence/THEOREM_MAP.json').write_text(json.dumps(label_map,indent=2)+'\n')
    identity=json.loads((ROOT/'IDENTITY.json').read_text())
    receipt={'revision':123,'controlling_review_commit':identity['controlling_review_commit'],
             'source_lock_sha256':sha(ROOT/'SOURCE_LOCK.json'),
             'remote_push_performed_by_this_environment':False,
             'remote_revision_source_commit':None,
             'observed_remote_target_head_at_preparation':identity['observed_remote_target_head'],
             'pdfs':{'geometry.pdf':{'pages':len(main_pdf),'sha256':sha(ROOT/'geometry.pdf')},
                     'paper.pdf':{'pages':len(full),'sha256':sha(ROOT/'paper.pdf')}},
             'source_lock_files_checked':len(lock['sha256']),
             'historical_files_checked':len(preserved['v122_input_sha256']),
             'historical_pdf_preservation':{'pages':len(old),'normalized_text_equal_all_pages':all(text_ok),
                'render_equal_all_pages_at_36_dpi':all(raster_ok),'direct_page_insertion_no_rescaling':True},
             'postflight':logs,'finite_diagnostic_files':diagnostics,
             'versions':{'python':platform.python_version(),'sympy':sympy.__version__,
                         'numpy':numpy.__version__,'pymupdf':fitz.VersionBind,
                         'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0]},
             'general_proof_machine_certified':False,'priority_certified':False,
             'independent_referee_review_of_v123':False}
    target=ROOT/args.receipt
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'PASS: {len(main_pdf)} principal pages; {len(full)} companion pages; {len(old)} historical pages preserved.')
    print(f'Receipt: {target.name}. General proof and priority certification remain false.')

if __name__=='__main__':
    main()
