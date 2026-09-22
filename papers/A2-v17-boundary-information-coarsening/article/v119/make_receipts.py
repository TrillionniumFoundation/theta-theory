#!/usr/bin/env python3
"""Receipt for files actually built locally; never a remote or proof certificate."""
from pathlib import Path
import hashlib,json,re,sys,subprocess
import fitz
here=Path(__file__).resolve().parent
files=[]
for p in here.rglob('*'):
    rel=p.relative_to(here)
    if not p.is_file() or rel.parts[0] in ('evidence','inherited-v118','crossrefs','__pycache__'): continue
    if p.suffix in ('.tex','.py','.sh','.md'):
        files.append(p)
manifest={str(p.relative_to(here)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(here/'evidence/SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
products={}
for name in ('geometry','paper','applications'):
    pdf=here/(name+'.pdf'); log=(here/(name+'.log')).read_text(errors='replace')
    fatal=re.findall(r'(?:LaTeX Warning: (?:There were undefined references|Label .*multiply defined)|! (?:LaTeX|Package)|Undefined control sequence)',log)
    unresolved=[x for x in log.splitlines() if 'undefined' in x.lower() and ('Reference' in x or 'Citation' in x)]
    overfull=re.findall(r'Overfull \\[hv]box.*',log)
    if fatal or unresolved: raise RuntimeError((name,fatal,unresolved))
    with fitz.open(pdf) as d: pages=len(d)
    products[name]={'pages':pages,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
                    'bytes':pdf.stat().st_size,'overfull_box_warnings':overfull,
                    'undefined_reference_or_citation_warnings':unresolved}
receipt={'kind':'actual local build receipt',
 'controlling_review_commit':'d4254d9b01405ad02c64d2ff591503d4cc7a6aa7',
 'reviewed_math_commit':'c87bfdad8d97e68637d269e656b46c4cce85551e',
 'reviewed_product_head':'44bfc648ead008896a6981a7302a6d5ab8b21bb8',
 'intended_remote_branch':'revision/a2-v119-codimension-primary-conductor-2026-09-22',
 'source_manifest_sha256':hashlib.sha256((here/'evidence/SOURCE_MANIFEST.json').read_bytes()).hexdigest(),
 'products':products,'python':sys.version,'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
 'remote_branch_created':False,'remote_push_performed':False,'proof_certification':False,
 'priority_certification':False,'Ballico_1993_full_text_comparison':'open'}
(here/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
